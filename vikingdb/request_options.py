# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass, field
from typing import MutableMapping, Optional


@dataclass
class RequestOptions:
    """
    Per-request overrides for headers, query parameters, and retry behaviour.

    Attributes:
        headers: Additional HTTP headers to apply for a single request.
        query: Additional query parameters appended to the request URL.
        request_id: Optional request identifier propagated via X-Tt-Logid.
        max_attempts: Override for retry attempts (defaults to client configuration).
        timeout: Override for the response read timeout (seconds).
    """

    headers: MutableMapping[str, str] = field(default_factory=dict)
    query: MutableMapping[str, str] = field(default_factory=dict)
    request_id: Optional[str] = None
    max_attempts: Optional[int] = None
    timeout: Optional[int] = None


def ensure_request_options(
    options: Optional[RequestOptions],
) -> RequestOptions:
    return options if options is not None else RequestOptions()
