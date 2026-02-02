# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Dict, Optional, Sequence, List

from pydantic import Field

from .base import DataApiResponse, Model
from .point import ChunkAttachment, PointTableChunkField
from .chat import ChatMessage

__all__ = [
    "ServiceChatRequest",
    "ServiceChatResponse",
    "ServiceChatData",
    "ServiceChatRetrieveItemDocInfo",
    "ServiceChatRetrieveItem",
]


class ServiceChatRequest(Model):
    service_resource_id: str = Field(alias="service_resource_id")
    messages: Sequence[ChatMessage] = Field(alias="messages")
    query_param: Optional[Dict[str, Any]] = Field(default=None, alias="query_param")
    stream: Optional[bool] = Field(default=False, alias="stream")


class ServiceChatRetrieveItemDocInfo(Model):
    doc_id: Optional[str] = Field(default=None, alias="doc_id")
    doc_name: Optional[str] = Field(default=None, alias="doc_name")
    create_time: Optional[int] = Field(default=None, alias="create_time")
    doc_type: Optional[str] = Field(default=None, alias="doc_type")
    doc_meta: Optional[str] = Field(default=None, alias="doc_meta")
    source: Optional[str] = Field(default=None, alias="source")
    title: Optional[str] = Field(default=None, alias="title")


class ServiceChatRetrieveItem(Model):
    id: Optional[str] = Field(default=None, alias="id")
    content: Optional[str] = Field(default=None, alias="content")
    md_content: Optional[str] = Field(default=None, alias="md_content")
    score: Optional[float] = Field(default=None, alias="score")
    point_id: Optional[str] = Field(default=None, alias="point_id")
    origin_text: Optional[str] = Field(default=None, alias="origin_text")
    original_question: Optional[str] = Field(default=None, alias="original_question")
    chunk_title: Optional[str] = Field(default=None, alias="chunk_title")
    chunk_id: Optional[int] = Field(default=None, alias="chunk_id")
    process_time: Optional[int] = Field(default=None, alias="process_time")
    rerank_score: Optional[float] = Field(default=None, alias="rerank_score")
    doc_info: Optional[ServiceChatRetrieveItemDocInfo] = Field(default=None, alias="doc_info")
    recall_position: Optional[int] = Field(default=None, alias="recall_position")
    rerank_position: Optional[int] = Field(default=None, alias="rerank_position")
    chunk_type: Optional[str] = Field(default=None, alias="chunk_type")
    chunk_source: Optional[str] = Field(default=None, alias="chunk_source")
    update_time: Optional[int] = Field(default=None, alias="update_time")
    chunk_attachment: Optional[List[ChunkAttachment]] = Field(default=None, alias="chunk_attachment")
    table_chunk_fields: Optional[List[PointTableChunkField]] = Field(default=None, alias="table_chunk_fields")
    original_coordinate: Optional[Dict[str, Any]] = Field(default=None, alias="original_coordinate")


class ServiceChatData(Model):
    # Retrieval-type fields
    count: Optional[int] = Field(default=None, alias="count")
    rewrite_query: Optional[str] = Field(default=None, alias="rewrite_query")
    token_usage: Optional[Any] = Field(default=None, alias="token_usage")
    result_list: List[ServiceChatRetrieveItem] = Field(default_factory=list, alias="result_list")
    # Generation-type fields (non-stream)
    generated_answer: Optional[str] = Field(default=None, alias="generated_answer")
    reasoning_content: Optional[str] = Field(default=None, alias="reasoning_content")
    prompt: Optional[str] = Field(default=None, alias="prompt")
    end: Optional[bool] = Field(default=None, alias="end")


class ServiceChatResponse(DataApiResponse):
    result: Optional[ServiceChatData] = None
