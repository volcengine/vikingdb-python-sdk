# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional, Union, List

from pydantic import Field

from .base import Model, DataApiResponse

__all__ = [
    "RerankDataItem",
    "RerankResult",
    "RerankResponse",
]

class RerankDataItem(Model):
    query: object = Field(alias="query")
    content: str = Field(alias="content")
    title: Optional[str] = Field(default=None, alias="title")
    image: Union[str, List[str]] = Field(default=None, alias="image")

class RerankResult(Model):
    scores: List[float] = Field(default_factory=list, alias="scores")
    token_usage: Optional[int] = Field(default=None, alias="token_usage")

class RerankResponse(DataApiResponse):
    result: Optional[RerankResult] = None

