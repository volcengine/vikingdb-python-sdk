# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
import random
import time
from typing import Any, Mapping, MutableMapping, Optional
from urllib.parse import urlencode, urljoin

import requests

from .config import ClientConfig
from .credentials import AuthStrategy
from .exceptions import HTTPError, TransportError
from .request_options import RequestOptions, ensure_request_options

_REQUEST_ID_HEADER = "X-Tt-Logid"


class Transport:
    """Low-level HTTP executor responsible for retries, auth, and JSON handling."""

    def __init__(
        self,
        config: ClientConfig,
        auth: AuthStrategy,
        session: Optional[requests.Session] = None,
    ) -> None:
        self._config = config
        self._auth = auth
        self._session = session or requests.Session()
        self._base_url = config.endpoint.rstrip("/")

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Optional[Mapping[str, Any]] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None,
        options: Optional[RequestOptions] = None,
    ) -> Mapping[str, Any]:
        request_options = ensure_request_options(options)
        url = self._build_url(path, params, request_options.query)
        base_headers = self._build_headers(headers, request_options)

        body_text: Optional[str] = None
        if json_body is not None:
            body_text = json.dumps(json_body, ensure_ascii=False, separators=(",", ":"))
            base_headers.setdefault("Content-Type", "application/json")

        max_attempts = request_options.max_attempts or self._config.retry.max_attempts
        if max_attempts < 1:
            max_attempts = 1

        attempt = 0
        delay = self._config.retry.initial_interval
        last_error: Optional[Exception] = None

        while attempt < max_attempts:
            attempt += 1
            prepared = self._prepare_request(method, url, body_text, base_headers)
            try:
                response = self._session.send(
                    prepared,
                    timeout=self._config.timeout,
                    verify=self._config.verify_ssl,
                    allow_redirects=False,
                )
            except requests.RequestException as exc:
                err = TransportError(str(exc), retryable=True)
                last_error = err
                if attempt >= max_attempts:
                    raise err
                self._sleep(delay)
                delay = self._next_delay(delay)
                continue

            if 200 <= response.status_code < 300:
                return self._parse_success(response)

            error = self._build_http_error(response)
            last_error = error
            if not error.retryable or attempt >= max_attempts:
                raise error

            self._sleep(delay)
            delay = self._next_delay(delay)

        if last_error:
            raise last_error
        raise TransportError("request failed without producing a response")

    def _prepare_request(
        self,
        method: str,
        url: str,
        body_text: Optional[str],
        headers: Mapping[str, str],
    ) -> requests.PreparedRequest:
        request = requests.Request(
            method=method.upper(),
            url=url,
            data=body_text.encode("utf-8") if isinstance(body_text, str) else None,
            headers=dict(headers),
        )
        prepared = self._session.prepare_request(request)
        # Apply authentication _after_ preparing the request so that headers are final.
        self._auth.apply(prepared)
        return prepared

    def _build_headers(
        self,
        headers: Optional[Mapping[str, str]],
        options: RequestOptions,
    ) -> MutableMapping[str, str]:
        merged: MutableMapping[str, str] = {
            "Accept": "application/json",
            "User-Agent": self._config.user_agent,
        }
        if options.request_id:
            merged[_REQUEST_ID_HEADER] = options.request_id
        if headers:
            merged.update(headers)
        if options.headers:
            merged.update(options.headers)
        return merged

    def _build_url(
        self,
        path: str,
        params: Optional[Mapping[str, str]],
        option_params: Mapping[str, str],
    ) -> str:
        normalized_path = path if path.startswith("/") else f"/{path}"
        base = urljoin(self._base_url + "/", normalized_path.lstrip("/"))
        combined_query: MutableMapping[str, str] = {}
        if params:
            combined_query.update(params)
        if option_params:
            combined_query.update(option_params)
        if not combined_query:
            return base
        return f"{base}?{urlencode(combined_query, doseq=True)}"

    @staticmethod
    def _parse_success(response: requests.Response) -> Mapping[str, Any]:
        if not response.content:
            return {}
        try:
            return json.loads(response.text)
        except json.JSONDecodeError as exc:  # pragma: no cover - unexpected data
            raise TransportError(f"failed to parse response JSON: {exc}") from exc

    def _build_http_error(self, response: requests.Response) -> HTTPError:
        retryable = response.status_code == 429 or response.status_code >= 500
        code: Optional[str] = None
        message: str = response.text or "HTTP request failed"
        request_id: Optional[str] = response.headers.get(_REQUEST_ID_HEADER)

        if response.headers.get("Content-Type", "").startswith("application/json"):
            try:
                payload = response.json()
                code = payload.get("code") or payload.get("Code")
                message = payload.get("message") or payload.get("Message") or message
                request_id = payload.get("request_id") or payload.get("RequestId") or request_id
            except ValueError:
                pass

        return HTTPError(
            message,
            status_code=response.status_code,
            code=code,
            request_id=request_id,
            retryable=retryable,
        )

    def _sleep(self, delay: float) -> None:
        jitter = self._config.retry.jitter
        if jitter > 0:
            factor = 1 - jitter + random.random() * (2 * jitter)
        else:
            factor = 1.0
        sleep_for = min(delay * factor, self._config.retry.max_interval)
        time.sleep(sleep_for)

    def _next_delay(self, current: float) -> float:
        next_delay = current * self._config.retry.multiplier
        return min(next_delay, self._config.retry.max_interval)

