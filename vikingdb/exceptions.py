from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Type, TypeVar, Union

DEFAULT_UNKNOWN_ERROR_CODE: Union[int, str] = 1000028
NETWORK_ERROR_CODE = 1001


@dataclass
class ParsedError:
    code: Union[int, str]
    request_id: str
    message: Optional[str]
    payload: Any
    raw: Optional[str] = None


def _normalize_code(value: Any, default: Union[int, str]) -> Union[int, str]:
    if value is None:
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_error_payload(payload: Any) -> ParsedError:
    """
    Parse a server error payload into a consistent structure.
    
    Supports both the legacy {"ResponseMetadata": {"Error": {...}}} format and the
    newer flat {"code": ..., "request_id": ..., "message": ...} shape. When JSON
    decoding fails, the raw text is preserved as the message.
    """
    code = DEFAULT_UNKNOWN_ERROR_CODE
    request_id = "unknown"
    message: Optional[str] = None
    raw_text: Optional[str] = None
    parsed_payload: Any = payload

    if isinstance(payload, bytes):
        raw_text = payload.decode("utf-8", errors="replace")
    elif isinstance(payload, str):
        raw_text = payload

    if raw_text is not None:
        try:
            parsed_payload = json.loads(raw_text)
        except json.JSONDecodeError:
            message = raw_text.strip() or None
            return ParsedError(code, request_id, message, raw_text, raw_text)

    if isinstance(parsed_payload, Mapping):
        metadata = parsed_payload.get("ResponseMetadata")
        if isinstance(metadata, Mapping):
            error = metadata.get("Error")
            if isinstance(error, Mapping):
                code_value = error.get("Code") if "Code" in error else error.get("code")
                code = _normalize_code(code_value, code)
                request_id = str(error.get("RequestId") or request_id)
                if error.get("Message"):
                    message = str(error["Message"])
            if metadata.get("RequestId"):
                request_id = str(metadata["RequestId"])
        else:
            code_value = parsed_payload.get("code")
            if code_value is None and "Code" in parsed_payload:
                code_value = parsed_payload.get("Code")
            code = _normalize_code(code_value, code)
            if parsed_payload.get("request_id"):
                request_id = str(parsed_payload["request_id"])
            if parsed_payload.get("message"):
                message = str(parsed_payload["message"])
    else:
        if message is None and raw_text is None:
            message = str(parsed_payload)

    if raw_text is None and isinstance(parsed_payload, (dict, list)):
        try:
            raw_text = json.dumps(parsed_payload, ensure_ascii=False)
        except Exception:
            raw_text = None

    return ParsedError(code, request_id, message, parsed_payload, raw_text)


T_VikingException = TypeVar("T_VikingException", bound="VikingException")


class VikingException(Exception):
    """
    Base exception for all Viking SDK errors.

    Captures standard fields returned by the service for consistent error handling.
    """

    def __init__(
        self,
        code: Union[int, str],
        request_id: str = "unknown",
        message: Optional[str] = None,
        *,
        status_code: Optional[int] = None,
    ) -> None:
        self.code = code
        self.request_id = request_id or "unknown"
        self.status_code = status_code
        self.message = message or f"request failed (code={self.code})"
        super().__init__(self.message)

    def __str__(self) -> str:
        status = f", http_status={self.status_code}" if self.status_code is not None else ""
        return f"{self.message} (code={self.code}, request_id={self.request_id}{status})"

    def promote(self, target_cls: Type[T_VikingException]) -> T_VikingException:
        """
        Promote this exception to a more specific subclass, reusing captured context.
        """
        if isinstance(self, target_cls):
            return self  # type: ignore[return-value]
        return target_cls(
            self.code,
            self.request_id,
            self.message,
            status_code=self.status_code,
        )


class VikingAPIException(VikingException):
    """Raised when the remote API returns an error payload."""

    @classmethod
    def from_response(cls, payload: Any, *, request_id: Optional[str] = "unknown", status_code: Optional[int] = None) -> "VikingAPIException":
        parsed = parse_error_payload(payload)
        return cls(
            parsed.code,
            parsed.request_id or request_id,
            parsed.message or "unknown api error",
            status_code=status_code,
        )


def promote_exception(
    exc: VikingException,
    *,
    exception_map: Optional[Mapping[int, Type[T_VikingException]]] = None,
    default_cls: Type[T_VikingException],
) -> T_VikingException:
    """
    Promote a VikingException to a service-specific subclass using the provided map.
    """
    target_cls = (exception_map or {}).get(exc.code, default_cls)
    return exc.promote(target_cls)
