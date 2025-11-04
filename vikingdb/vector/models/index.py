# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence

from pydantic import Field

from .base import DataApiResponse, Model
from .collection import DataItem


class FetchDataInIndexRequest(Model):
    ids: Sequence[Any] = Field(alias="ids")
    partition: Optional[str] = Field(default=None, alias="partition")
    output_fields: Optional[Sequence[str]] = Field(default=None, alias="output_fields")


class IndexDataItem(DataItem):
    dense_dim: Optional[int] = Field(default=None, alias="dense_dim")
    dense_vector: Optional[List[float]] = Field(default=None, alias="dense_vector")


class FetchDataInIndexResult(Model):
    items: List[IndexDataItem] = Field(default_factory=list, alias="fetch")
    ids_not_exist: List[Any] = Field(default_factory=list, alias="ids_not_exist")


class FetchDataInIndexResponse(DataApiResponse):
    result: Optional[FetchDataInIndexResult] = None


class SearchAdvance(Model):
    dense_weight: Optional[float] = Field(default=None, alias="dense_weight")
    ids_in: Optional[Sequence[Any]] = Field(default=None, alias="ids_in")
    ids_not_in: Optional[Sequence[Any]] = Field(default=None, alias="ids_not_in")
    post_process_ops: Optional[Sequence[Mapping[str, Any]]] = Field(default=None, alias="post_process_ops")
    post_process_input_limit: Optional[int] = Field(default=None, alias="post_process_input_limit")
    scale_k: Optional[float] = Field(default=None, alias="scale_k")
    filter_pre_ann_limit: Optional[int] = Field(default=None, alias="filter_pre_ann_limit")
    filter_pre_ann_ratio: Optional[float] = Field(default=None, alias="filter_pre_ann_ratio")


class RecallBase(Model):
    filter: Optional[Mapping[str, Any]] = Field(default=None, alias="filter")
    partition: Optional[str] = Field(default=None, alias="partition")


class SearchBase(RecallBase):
    output_fields: Optional[Sequence[str]] = Field(default=None, alias="output_fields")
    limit: Optional[int] = Field(default=None, alias="limit")
    offset: Optional[int] = Field(default=None, alias="offset")
    advance: Optional[SearchAdvance] = Field(default=None, alias="advance")


class SearchItemResult(Model):
    id: Any = Field(alias="id")
    fields: Dict[str, Any] = Field(default_factory=dict, alias="fields")
    ann_score: Optional[float] = Field(default=None, alias="ann_score")
    score: Optional[float] = Field(default=None, alias="score")


class SearchResult(Model):
    data: List[SearchItemResult] = Field(default_factory=list, alias="data")
    filter_matched_count: Optional[int] = Field(default=None, alias="filter_matched_count")
    total_return_count: Optional[int] = Field(default=None, alias="total_return_count")
    real_text_query: Optional[str] = Field(default=None, alias="real_text_query")
    token_usage: Dict[str, Any] = Field(default_factory=dict, alias="token_usage")


class SearchResponse(DataApiResponse):
    result: Optional[SearchResult] = None


class SearchByVectorRequest(SearchBase):
    dense_vector: Sequence[float] = Field(alias="dense_vector")
    sparse_vector: Optional[Mapping[str, float]] = Field(default=None, alias="sparse_vector")


class SearchByMultiModalRequest(SearchBase):
    text: Optional[str] = Field(default=None, alias="text")
    image: Optional[Any] = Field(default=None, alias="image")
    video: Optional[Any] = Field(default=None, alias="video")
    need_instruction: Optional[bool] = Field(default=None, alias="need_instruction")


class SearchByIDRequest(SearchBase):
    id: Any = Field(alias="id")


class SearchByScalarRequest(SearchBase):
    field: Optional[str] = Field(default=None, alias="field")
    order: Optional[str] = Field(default=None, alias="order")


class SearchByKeywordsRequest(SearchBase):
    keywords: Optional[Sequence[str]] = Field(default=None, alias="keywords")
    query: Optional[str] = Field(default=None, alias="query")
    case_sensitive: Optional[bool] = Field(default=None, alias="case_sensitive")


class SearchByRandomRequest(SearchBase):
    pass


class AggRequest(RecallBase):
    op: str = Field(alias="op")
    field: Optional[str] = Field(default=None, alias="field")
    cond: Optional[Mapping[str, Any]] = Field(default=None, alias="cond")
    order: Optional[str] = Field(default=None, alias="order")


class AggResult(Model):
    agg: Dict[str, Any] = Field(default_factory=dict, alias="agg")
    op: Optional[str] = Field(default=None, alias="op")
    field: Optional[str] = Field(default=None, alias="field")


class AggResponse(DataApiResponse):
    result: Optional[AggResult] = None

