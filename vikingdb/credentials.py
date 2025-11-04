# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections import OrderedDict
from typing import Optional
from urllib.parse import parse_qsl, urlparse

import requests
from volcengine.Credentials import Credentials as VolcCredentials
from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Request import Request as SigningRequest


class AuthStrategy:
    """Strategy interface for applying authentication to outgoing HTTP requests."""

    def apply(self, request: requests.PreparedRequest) -> None:
        raise NotImplementedError

class APIKey(AuthStrategy):
    """Injects an API key as a bearer token."""

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("api_key must be provided")
        self._api_key = api_key

    def apply(self, request: requests.PreparedRequest) -> None:
        request.headers["Authorization"] = f"Bearer {self._api_key}"


class IAM(AuthStrategy):
    """Signs requests using Volcano Engine V4 credentials.

    The region is supplied by :class:`vikingdb.vector.VikingDB` during client construction.
    When using (usually don't) this strategy outside of the high-level client,
    call :meth:`configure` with the desired region before issuing requests.
    """

    def __init__(
        self,
        access_key: str,
        secret_key: str,
    ) -> None:
        if not access_key or not secret_key:
            raise ValueError("access_key and secret_key must be provided")
        self._access_key = access_key
        self._secret_key = secret_key
        self._service = "vikingdb"  # fixed as this pkg is only for VikingDB
        self._credentials: Optional[VolcCredentials] = None
        self._region: Optional[str] = None

    def configure(self, *, region: str) -> None:
        if not region:
            raise ValueError("region must be provided to configure IAM credentials")
        self._region = region
        self._credentials = VolcCredentials(self._access_key, self._secret_key, self._service, region)

    def apply(self, request: requests.PreparedRequest) -> None:
        if self._credentials is None:
            raise ValueError("IAM credentials require a configured region before use")
        parsed = urlparse(request.url)
        signing_request = SigningRequest()
        signing_request.set_schema(parsed.scheme or "https")
        signing_request.set_host(parsed.netloc)
        signing_request.set_path(parsed.path or "/")
        signing_request.set_method(request.method or "GET")
        signing_request.set_headers(OrderedDict(request.headers.items()))
        signing_request.set_query(OrderedDict(parse_qsl(parsed.query, keep_blank_values=True)))

        body = request.body
        if isinstance(body, bytes):
            body_str = body.decode("utf-8")
        elif body is None:
            body_str = ""
        else:
            body_str = str(body)
        signing_request.set_body(body_str)

        SignerV4.sign(signing_request, self._credentials)
        for header, value in signing_request.headers.items():
            request.headers[header] = value
