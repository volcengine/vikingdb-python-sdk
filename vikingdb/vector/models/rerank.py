# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from pydantic import Field

from .base import DataApiResponse, Model
from .embedding import FullModalData


class RerankRequest(Model):
    model_name: Optional[str] = Field(alias="model_name")
    model_version: Optional[str] = Field(default=None, alias="model_version")
    data: Sequence[Sequence[FullModalData]] = Field(alias="data")
    query: Sequence[FullModalData] = Field(alias="query")
    instruction: Optional[str] = Field(default=None, alias="instruction")
    return_origin_data: Optional[bool] = Field(default=None, alias="return_origin_data")


class RerankResult(Model):
    data: List[Rerank] = Field(default_factory=list, alias="data")
    token_usage: Dict[str, Any] = Field(default_factory=dict, alias="token_usage")


class Rerank(Model):
    id: Optional[int] = Field(default=None, alias="id")
    score: Optional[float] = Field(default=None, alias="score")
    origin_data: Sequence[FullModalData] = Field(default=None, alias="origin_data")


class RerankResponse(DataApiResponse):
    result: Optional[RerankResult] = None
