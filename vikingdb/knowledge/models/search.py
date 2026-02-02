# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from pydantic import Field

from .base import DataApiResponse, Model
from .point import PointInfo

__all__ = [
    "SearchCollectionRequest",
    "SearchResult",
    "SearchResponse",
    "SearchKnowledgeRequest",
    "SearchKnowledgeResult",
    "SearchKnowledgeResponse",
]

class SearchCollectionRequest(Model):
    query: Any = Field(alias="query")
    limit: int = Field(default=10, alias="limit")
    dense_weight: float = Field(default=0.5, alias="dense_weight")
    rerank_switch: bool = Field(default=False, alias="rerank_switch")
    query_param: Optional[Dict[str, Any]] = Field(default=None, alias="query_param")
    retrieve_count: Optional[int] = Field(default=None, alias="retrieve_count")
    endpoint_id: Optional[str] = Field(default=None, alias="endpoint_id")
    rerank_model: Optional[str] = Field(default="Doubao-pro-4k-rerank", alias="rerank_model")
    rerank_only_chunk: bool = Field(default=False, alias="rerank_only_chunk")

class SearchResult(Model):
    result_list: List[PointInfo] = Field(default_factory=list, alias="result_list")


class SearchResponse(DataApiResponse):
    result: Optional[SearchResult] = None


class SearchKnowledgeRequest(Model):
    query: Any = Field(alias="query")
    image_query: Optional[Any] = Field(default=None, alias="image_query")
    pre_processing: Optional[Dict[str, Any]] = Field(default=None, alias="pre_processing")
    post_processing: Optional[Dict[str, Any]] = Field(default=None, alias="post_processing")
    query_param: Optional[Dict[str, Any]] = Field(default=None, alias="query_param")
    limit: int = Field(default=10, alias="limit")
    dense_weight: float = Field(default=0.5, alias="dense_weight")

class SearchKnowledgeResult(Model):
    count: Optional[int] = Field(default=None, alias="count")
    rewrite_query: Optional[str] = Field(default=None, alias="rewrite_query")
    token_usage: Dict[str, Any] = Field(default_factory=dict, alias="token_usage")
    result_list: List[PointInfo] = Field(default_factory=list, alias="result_list")

class SearchKnowledgeResponse(DataApiResponse):
    result: Optional[SearchKnowledgeResult] = None
