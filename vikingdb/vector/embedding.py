# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Mapping, Optional, Union, cast

from ..request_options import RequestOptions
from .base import VectorClientBase
from .models import EmbeddingRequest, EmbeddingResponse


class EmbeddingClient(VectorClientBase):
    """Client for VikingDB embedding APIs."""

    def embedding(
        self,
        request: Union[EmbeddingRequest, Mapping[str, object]],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> EmbeddingResponse:
        payload = self._merge_payload({}, request)
        response = cast(
            EmbeddingResponse,
            self._post(
                "/api/vikingdb/embedding",
                payload,
                EmbeddingResponse,
                request_options=request_options,
            ),
        )
        return response
