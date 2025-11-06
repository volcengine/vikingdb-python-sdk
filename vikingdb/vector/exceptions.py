# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional, Union

from ..exceptions import VikingException

class VikingConnectionException(Exception):
    def __init__(self, msg: str, cause: str) -> None:
        super().__init__(msg, cause)
        

class VikingVectorException(VikingException):
    """Raised when the remote VikingDB service returns an error payload."""

    def __init__(
        self,
        code: Union[int, str],  # to satisfy VikingException, but we normalise to str when needed
        request_id: str = "unknown",
        message: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> None:
        if isinstance(code, int):
            code = f"InternalServerError({code})"
        resolved_message = (
            message
            or f"request failed with code={code!r}, request_id={request_id}"
        )
        super().__init__(
            code,
            request_id,
            resolved_message,
            status_code=status_code,
        )

    def __str__(self) -> str:
        status = f", http_status={self.status_code}" if self.status_code is not None else ""
        return f"{self.message} (code={self.code!r}, request_id={self.request_id}{status})"
