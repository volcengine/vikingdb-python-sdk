# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""Common authentication helpers shared by Viking services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from volcengine.Credentials import Credentials
from volcengine.auth.SignerV4 import SignerV4


class Auth(ABC):
    """Base class for authentication providers compatible with volcengine."""

    @abstractmethod
    def initialize(self, *, service: str, region: str):
        """Prepare the provider for the given service/region. Returns credentials understood by ServiceInfo."""

    @abstractmethod
    def sign_request(self, request) -> None:
        """Sign or otherwise authorise the outgoing request."""


class IAM(Auth):
    """IAM-style AK/SK signature authentication provider."""

    def __init__(self, *, ak: str, sk: str):
        if not ak or not sk:
            raise ValueError("ak and sk must be provided for IAM authentication")
        self._ak = ak
        self._sk = sk
        self._credentials = None
        self._service = None
        self._region = None

    def initialize(self, *, service: str, region: str):
        if not service or not region:
            raise ValueError("service and region must be provided for IAM credentials")
        if self._credentials is not None and (service != self._service or region != self._region):
            raise ValueError(
                f"IAM credentials already initialised for service={self._service!r}, region={self._region!r}"
            )
        self._service = service
        self._region = region
        if self._credentials is None:
            self._credentials = Credentials(self._ak, self._sk, service, region)
        return self._credentials

    def sign_request(self, request) -> None:
        if self._credentials is None:
            raise ValueError("IAM provider must be initialised before signing requests")
        SignerV4.sign(request, self._credentials)


class APIKey(Auth):
    """API Key authentication provider (placeholder for future support)."""

    def __init__(self, *, api_key: str):
        if not api_key:
            raise ValueError("api_key must be provided for API key authentication")
        self.api_key = api_key

    def initialize(self, *, service: str, region: str):
        return None

    def sign_request(self, request) -> None:
        request.headers["Authorization"] = f"Bearer {self.api_key}"
