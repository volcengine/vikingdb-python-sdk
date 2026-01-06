# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Mapping, Optional, Union, cast

from ..request_options import RequestOptions
from .base import VectorClientBase
from .client import API_VECTOR_RERANK
from .models import RerankRequest, RerankResponse


class RerankClient(VectorClientBase):
    """Client for VikingDB rerank APIs."""

    def rerank(
        self,
        request: Union[RerankRequest, Mapping[str, object]],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> RerankResponse:
        payload = self._merge_payload({}, request)
        response = cast(
            RerankResponse,
            self._post(
                API_VECTOR_RERANK,
                payload,
                RerankResponse,
                request_options=request_options,
            ),
        )
        return response
