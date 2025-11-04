# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass, field

from .version import __version__


DEFAULT_USER_AGENT = f"vikingdb-python-sdk/{__version__}"


@dataclass(frozen=True)
class RetryConfig:
    """
    Retry strategy configuration.

    Attributes:
        max_attempts: Total number of attempts (initial call + retries).
        initial_interval: Initial backoff delay in seconds.
        max_interval: Maximum allowed delay between attempts in seconds.
        multiplier: Backoff multiplier applied after each retry.
        jitter: Randomisation factor applied to each backoff delay (0.0-1.0).
    """

    max_attempts: int = 3
    initial_interval: float = 0.5
    max_interval: float = 8.0
    multiplier: float = 2.0
    jitter: float = 0.25


@dataclass
class ClientConfig:
    """
    Shared configuration for all VikingDB clients.

    Attributes:
        endpoint: Base URL for the VikingDB API (e.g. https://api.vector.bytedance.com).
        region: Region used when signing requests (default cn-beijing).
        timeout: Request timeout in seconds (applies to both connect/read).
        retry: Retry strategy applied to idempotent API calls.
        user_agent: Custom user agent header; defaults to the SDK identifier.
        verify_ssl: Whether to verify TLS certificates.
    """

    endpoint: str
    region: str = "cn-beijing"
    timeout: float = 30.0
    retry: RetryConfig = field(default_factory=RetryConfig)
    user_agent: str = DEFAULT_USER_AGENT
    verify_ssl: bool = True

    def __post_init__(self) -> None:
        if not self.endpoint:
            raise ValueError("endpoint must be provided")
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        if self.retry.max_attempts < 1:
            raise ValueError("retry.max_attempts must be at least 1")
        if self.retry.initial_interval <= 0 or self.retry.max_interval <= 0:
            raise ValueError("retry intervals must be positive")
        if self.retry.multiplier < 1.0:
            raise ValueError("retry.multiplier must be >= 1.0")
        if not (0.0 <= self.retry.jitter < 1.0):
            raise ValueError("retry.jitter must be in range [0.0, 1.0)")
