"""Shared base client logic for Viking services."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional

import aiohttp

from volcengine.ApiInfo import ApiInfo
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Request import Request
from volcengine.base.Service import Service

from .auth import Auth


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
        connection_timeout: int = 30,
        socket_timeout: int = 30,
    ):
        self.region = region
        self.service = service
        self.auth_provider = auth
        credentials = auth.initialize(service=service, region=region)
        self.service_info = self._build_service_info(
            host=host,
            credentials=credentials,
            scheme=scheme,
            connection_timeout=connection_timeout,
            socket_timeout=socket_timeout,
        )
        self.api_info = self._build_api_info()
        super().__init__(self.service_info, self.api_info)

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
        connection_timeout: int,
        socket_timeout: int,
    ) -> ServiceInfo:
        return ServiceInfo(
            host,
            {},
            credentials,
            connection_timeout,
            socket_timeout,
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
    ) -> str:
        """Send a JSON request synchronously."""
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
        response = self.session.post(
            url,
            headers=request.headers,
            data=request.body,
            timeout=(
                self.service_info.connection_timeout,
                self.service_info.socket_timeout,
            ),
        )
        if response.status_code == 200:
            return json.dumps(response.json())
        raise Exception(response.text.encode("utf-8"))

    async def async_json(
        self,
        api: str,
        params: Optional[Mapping[str, Any]],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> str:
        """Send a JSON request asynchronously."""
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
        timeout = aiohttp.ClientTimeout(
            connect=self.service_info.connection_timeout,
            sock_connect=self.service_info.socket_timeout,
        )
        url = request.build()
        async with aiohttp.request(
            "POST",
            url,
            headers=request.headers,
            data=request.body,
            timeout=timeout,
        ) as response:
            payload = await response.text(encoding="utf-8")
            if response.status == 200:
                return payload
            raise Exception(payload)
