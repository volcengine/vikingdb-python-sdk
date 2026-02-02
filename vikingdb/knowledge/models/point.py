# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from pydantic import Field

from .base import DataApiResponse, Model
from .doc import DocStatus

__all__ = [
    "AddPointRequest",
    "PointAddResult",
    "PointAddResponse",
    "UpdatePointRequest",
    "ListPointsRequest",
    "DeletePointRequest",
    "PointDocInfo",
    "ChunkAttachment",
    "PointTableChunkField",
    "PointInfo",
    "ListPointsResult",
    "ListPointsResponse",
]

class AddPointRequest(Model):
    doc_id: str = Field(alias="doc_id")
    chunk_type: str = Field(alias="chunk_type")
    chunk_title: Optional[str] = Field(default=None, alias="chunk_title")
    content: Optional[str] = Field(default=None, alias="content")
    question: Optional[str] = Field(default=None, alias="question")
    fields: Optional[List[Dict[str, Any]]] = Field(default=None, alias="fields")

class PointAddResult(Model):
    collection_name: Optional[str] = Field(default=None, alias="collection_name")
    project: Optional[str] = Field(default=None, alias="project")
    resource_id: Optional[str] = Field(default=None, alias="resource_id")
    doc_id: Optional[str] = Field(default=None, alias="doc_id")
    chunk_id: Optional[int] = Field(default=None, alias="chunk_id")
    point_id: Optional[str] = Field(default=None, alias="point_id")

class PointAddResponse(DataApiResponse):
    result: Optional[PointAddResult] = None

class UpdatePointRequest(Model):
    chunk_title: Optional[str] = Field(default=None, alias="chunk_title")
    content: Optional[str] = Field(default=None, alias="content")
    question: Optional[str] = Field(default=None, alias="question")
    fields: Optional[List[Dict[str, Any]]] = Field(default=None, alias="fields")

class ListPointsRequest(Model):
    offset: int = Field(default=0, alias="offset")
    limit: int = Field(default=-1, alias="limit")
    doc_ids: Optional[Dict[str, Any]] = Field(default=None, alias="doc_ids")
    point_ids: Optional[Dict[str, Any]] = Field(default=None, alias="point_ids")
    get_attachment_link: Optional[bool] = Field(default=False, alias="get_attachment_link")

class DeletePointRequest(Model):
    point_id: str = Field(alias="point_id")

class PointDocInfo(Model):
    doc_id: Optional[str] = Field(default=None, alias="doc_id")
    doc_name: Optional[str] = Field(default=None, alias="doc_name")
    create_time: Optional[int] = Field(default=None, alias="create_time")
    doc_type: Optional[str] = Field(default=None, alias="doc_type")
    doc_meta: Optional[str] = Field(default=None, alias="doc_meta")
    source: Optional[str] = Field(default=None, alias="source")
    title: Optional[str] = Field(default=None, alias="title")
    status: Optional[DocStatus] = Field(default=None, alias="status")

class ChunkAttachment(Model):
    uuid: Optional[str] = Field(default=None, alias="uuid")
    caption: Optional[str] = Field(default=None, alias="caption")
    type: Optional[str] = Field(default=None, alias="type")
    link: Optional[str] = Field(default=None, alias="link")
    info_link: Optional[str] = Field(default=None, alias="info_link")
    column_name: Optional[str] = Field(default=None, alias="column_name")

class PointTableChunkField(Model):
    field_name: Optional[str] = Field(default=None, alias="field_name")
    field_value: Optional[Any] = Field(default=None, alias="field_value")


class PointInfo(Model):
    collection_name: Optional[str] = Field(default=None, alias="collection_name")
    point_id: Optional[str] = Field(default=None, alias="point_id")
    process_time: Optional[int] = Field(default=None, alias="process_time")
    origin_text: Optional[str] = Field(default=None, alias="origin_text")
    md_content: Optional[str] = Field(default=None, alias="md_content")
    html_content: Optional[str] = Field(default=None, alias="html_content")
    chunk_title: Optional[str] = Field(default=None, alias="chunk_title")
    chunk_type: Optional[str] = Field(default=None, alias="chunk_type")
    content: Optional[str] = Field(default=None, alias="content")
    chunk_id: Optional[int] = Field(default=None, alias="chunk_id")
    original_question: Optional[str] = Field(default=None, alias="original_question")
    doc_info: Optional[PointDocInfo] = Field(default=None, alias="doc_info")
    rerank_score: Optional[float] = Field(default=None, alias="rerank_score")
    score: Optional[float] = Field(default=None, alias="score")
    chunk_source: Optional[str] = Field(default=None, alias="chunk_source")
    chunk_attachment: Optional[List[ChunkAttachment]] = Field(default=None, alias="chunk_attachment")
    table_chunk_fields: Optional[List[PointTableChunkField]] = Field(default=None, alias="table_chunk_fields")
    update_time: Optional[int] = Field(default=None, alias="update_time")
    description: Optional[str] = Field(default=None, alias="description")
    chunk_status: Optional[str] = Field(default=None, alias="chunk_status")
    video_frame: Optional[str] = Field(default=None, alias="video_frame")
    video_url: Optional[str] = Field(default=None, alias="video_url")
    video_start_time: Optional[int] = Field(default=None, alias="video_start_time")
    video_end_time: Optional[int] = Field(default=None, alias="video_end_time")
    video_outline: Optional[Dict[str, Any]] = Field(default=None, alias="video_outline")
    audio_start_time: Optional[int] = Field(default=None, alias="audio_start_time")
    audio_end_time: Optional[int] = Field(default=None, alias="audio_end_time")
    audio_outline: Optional[Dict[str, Any]] = Field(default=None, alias="audio_outline")
    sheet_name: Optional[str] = Field(default=None, alias="sheet_name")
    project: Optional[str] = Field(default="default", alias="project")
    resource_id: Optional[str] = Field(default=None, alias="resource_id")


class ListPointsResult(Model):
    point_list: Sequence[PointInfo] = Field(default_factory=list, alias="point_list")


class ListPointsResponse(DataApiResponse):
    result: Optional[ListPointsResult] = None
    count: Optional[int] = Field(default=None, alias="count")
    total_num: Optional[int] = Field(default=None, alias="total_num")
