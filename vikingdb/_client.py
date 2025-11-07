# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""Shared base client logic for Viking services."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from json import JSONDecodeError
from typing import Any, Mapping, Optional

import aiohttp

from volcengine.ApiInfo import ApiInfo
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Request import Request
from volcengine.base.Service import Service
import requests

from .auth import Auth, IAM, APIKey
from .exceptions import (
    DEFAULT_UNKNOWN_ERROR_CODE,
    VikingAPIException,
)


_REQUEST_ID_HEADER = "X-Tt-Logid"


class Client(Service, ABC):
    """Reusable base client built on top of volcengine Service."""

    def __init__(
        self,
        *,
        host: str,
        region: str,
        service: str,
        auth: Auth,
        sts_token: str = "",
        scheme: str = "http",
        timeout: int = 30,
    ):
        self.region = region
        self.service = service
        self.auth_provider = auth
        credentials = auth.initialize(service=service, region=region)
        self.service_info = self._build_service_info(
            host=host,
            credentials=credentials,
            scheme=scheme,
            timeout=timeout,
        )
        self.api_info = self._build_api_info()
        # 判断auth是不是IAM 还是 APIKey类型
        if isinstance(auth, IAM):
            super().__init__(self.service_info, self.api_info)
        elif isinstance(auth, APIKey):
            self.session = requests.session()
        else:
            raise ValueError("auth must be IAM or APIKey type")

        if sts_token:
            self.set_session_token(session_token=sts_token)

    @abstractmethod
    def _build_api_info(self) -> Mapping[str, ApiInfo]:
        """Return the API metadata mapping used by this client."""

    @staticmethod
    def _build_service_info(
        *,
        host: str,
        credentials,
        scheme: str,
        timeout: int,
    ) -> ServiceInfo:
        return ServiceInfo(
            host,
            {},
            credentials,
            timeout,
            timeout,
            scheme=scheme,
        )

    def prepare_request(self, api_info: ApiInfo, params: Optional[Mapping[str, Any]], doseq: int = 0):
        """Prepare a volcengine request without adding implicit headers."""
        request = Request()
        request.set_shema(self.service_info.scheme)
        request.set_method(api_info.method)
        request.set_host(self.service_info.host)
        request.set_path(api_info.path)
        request.set_connection_timeout(self.service_info.connection_timeout)
        request.set_socket_timeout(self.service_info.socket_timeout)
        request.set_headers(dict(api_info.header))
        if params:
            request.set_query(params)
        return request

    def _json(
        self,
        api: str,
        params: Optional[Mapping[str, Any]],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Any:
        """Send a JSON request synchronously.
        
        Args:
            api: API name
            params: Query parameters
            body: Request body
            headers: Additional headers
            timeout: Timeout in seconds (optional). If not provided, uses default connection_timeout and socket_timeout.
        """
        if api not in self.api_info:
            raise Exception("no such api")
        api_info = self.api_info[api]
        request = self.prepare_request(api_info, params)
        if headers:
            for key, value in headers.items():
                request.headers[key] = value
        request.headers["Content-Type"] = "application/json"
        request.body = body
        self.auth_provider.sign_request(request)
        url = request.build()
        
        request_id_value = request.headers.get(_REQUEST_ID_HEADER)
        request_id = str(request_id_value) if request_id_value else "unknown"
        
        # Use custom timeout if provided, otherwise use default
        if timeout is not None:
            request_timeout = (timeout, timeout)
        else:
            request_timeout = (
                self.service_info.connection_timeout,
                self.service_info.socket_timeout,
            )
        
        try:
            response = self.session.post(
                url,
                headers=request.headers,
                data=request.body,
                timeout=request_timeout,
            )
        except Exception as exc:
            raise VikingAPIException(
                    DEFAULT_UNKNOWN_ERROR_CODE,
                    request_id=request_id,
                    message=f"failed to run session.post {api}: {exc}",
                ) from exc

        payload_text_attr = getattr(response, "text", "")
        payload_text = payload_text_attr if isinstance(payload_text_attr, str) else ""
        payload_text = payload_text or ""

        if response.status_code != 200:
            error = VikingAPIException.from_response(
                payload_text,
                request_id=request_id,
                status_code=response.status_code,
            )
            raise error

        try:
            return response.json()
        except (ValueError, JSONDecodeError) as exc:
            raise VikingAPIException(
                DEFAULT_UNKNOWN_ERROR_CODE,
                request_id=request_id,
                message=f"failed to decode JSON response for {api}: {exc}",
                status_code=response.status_code,
            ) from exc

        except Exception as exc:  # pragma: no cover - defensive fallback
            raise VikingAPIException(
                DEFAULT_UNKNOWN_ERROR_CODE,
                request_id=request_id,
                message=f"unexpected error parsing response for {api}: {exc}",
                status_code=response.status_code,
            ) from exc

    async def async_json(
        self,
        api: str,
        params: Optional[Mapping[str, Any]],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Any:
        """Send a JSON request asynchronously.
        
        Args:
            api: API name
            params: Query parameters
            body: Request body
            headers: Additional headers
            timeout: Timeout in seconds (optional). If not provided, uses default connection_timeout and socket_timeout.
        """
        if api not in self.api_info:
            raise Exception("no such api")
        api_info = self.api_info[api]
        request = self.prepare_request(api_info, params)
        if headers:
            for key, value in headers.items():
                request.headers[key] = value
        request.headers["Content-Type"] = "application/json"
        request.body = body

        self.auth_provider.sign_request(request)
        
        # Use custom timeout if provided, otherwise use default
        if timeout is not None:
            client_timeout = aiohttp.ClientTimeout(
                connect=timeout,
                sock_connect=timeout,
                sock_read=timeout,
            )
        else:
            client_timeout = aiohttp.ClientTimeout(
                connect=self.service_info.connection_timeout,
                sock_connect=self.service_info.socket_timeout,
            )
        
        url = request.build()
        try:
            async with aiohttp.request(
                "POST",
                url,
                headers=request.headers,
                data=request.body,
                timeout=client_timeout,
            ) as response:
                request_id_value = response.headers.get(_REQUEST_ID_HEADER)
                request_id = str(request_id_value) if request_id_value else "unknown"
                payload = await response.text(encoding="utf-8")
                if response.status != 200:
                    error = VikingAPIException.from_response(
                        payload,
                        request_id=request_id,
                        status_code=response.status,
                    )
                    raise error
                try:
                    return json.loads(payload)
                except JSONDecodeError as exc:
                    raise VikingAPIException(
                        DEFAULT_UNKNOWN_ERROR_CODE,
                        request_id=request_id,
                        message=f"failed to decode JSON response for {api}: {exc}",
                        status_code=response.status,
                    ) from exc
        except Exception as exc:
            raise VikingAPIException(
                    DEFAULT_UNKNOWN_ERROR_CODE,
                    request_id=request_id,
                    message=f"failed to run aiohttp {api}: {exc}",
                ) from exc
