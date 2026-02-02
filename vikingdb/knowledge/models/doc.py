# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from pydantic import Field

from .base import DataApiResponse, Model

__all__ = [
    "AddDocRequest",
    "ListDocsRequest",
    "MetaItem",
    "DedupOptions",
    "DedupInfo",
    "AddDocV2Request",
    "DocStatus",
    "DocPremiumStatus",
    "DocInfo",
    "DocInfo",
    "ListDocsResult",
    "ListDocsResponse",
    "AddDocResponseData",
    "AddDocResponse",
]

class ListDocsRequest(Model):
    offset: int = Field(default=0, alias="offset")
    limit: int = Field(default=-1, alias="limit")
    doc_type: Optional[str] = Field(default=None, alias="doc_type")
    filter: Optional[Dict[str, Any]] = Field(default=None, alias="filter")
    return_token_usage: Optional[bool] = Field(default=False, alias="return_token_usage")

class AddDocRequest(Model):
    add_type: str = Field(alias="add_type")
    doc_id: Optional[str] = Field(default=None, alias="doc_id")
    doc_name: Optional[str] = Field(default=None, alias="doc_name")
    doc_type: Optional[str] = Field(default=None, alias="doc_type")
    description: Optional[str] = Field(default=None, alias="description")
    tos_path: Optional[str] = Field(default=None, alias="tos_path")
    url: Optional[str] = Field(default=None, alias="url")
    lark_file: Optional[str] = Field(default=None, alias="lark_file")
    meta: Optional[List["MetaItem"]] = Field(default=None, alias="meta")
    dedup: Optional["DedupOptions"] = Field(default=None, alias="dedup")

class DedupOptions(Model):
    content_dedup: Optional[bool] = Field(default=None, alias="content_dedup")
    doc_name_dedup: Optional[bool] = Field(default=None, alias="doc_name_dedup")
    auto_skip: Optional[bool] = Field(default=None, alias="auto_skip")

class MetaItem(Model):
    field_name: Optional[str] = Field(default=None, alias="field_name")
    field_type: Optional[str] = Field(default=None, alias="field_type")
    field_value: Optional[Any] = Field(default=None, alias="field_value")

class AddDocV2Request(Model):
    doc_id: Optional[str] = Field(default=None, alias="doc_id")
    doc_name: Optional[str] = Field(default=None, alias="doc_name")
    doc_type: Optional[str] = Field(default=None, alias="doc_type")
    description: Optional[str] = Field(default=None, alias="description")
    tag_list: Optional[List[MetaItem]] = Field(default=None, alias="tag_list")
    uri: Optional[str] = Field(default=None, alias="uri")

class DedupInfo(Model):
    skip: Optional[bool] = Field(default=None, alias="skip")
    same_doc_ids: Optional[List[str]] = Field(default=None, alias="same_doc_ids")

class DocStatus(Model):
    process_status: Optional[int] = Field(default=None, alias="process_status")
    failed_code: Optional[int] = Field(default=None, alias="failed_code")
    failed_msg: Optional[str] = Field(default=None, alias="failed_msg")

class DocPremiumStatus(Model):
    doc_summary_status_code: Optional[int] = Field(default=None, alias="doc_summary_status_code")


class DocInfo(Model):
    collection_name: Optional[str] = Field(default=None, alias="collection_name")
    doc_name: Optional[str] = Field(default=None, alias="doc_name")
    doc_id: Optional[str] = Field(default=None, alias="doc_id")
    doc_hash: Optional[str] = Field(default=None, alias="doc_hash")
    add_type: Optional[str] = Field(default=None, alias="add_type")
    doc_type: Optional[str] = Field(default=None, alias="doc_type")
    doc_summary: Optional[str] = Field(default=None, alias="doc_summary")
    brief_summary: Optional[str] = Field(default=None, alias="brief_summary")
    doc_size: Optional[int] = Field(default=None, alias="doc_size")
    description: Optional[str] = Field(default=None, alias="description")
    create_time: Optional[int] = Field(default=None, alias="create_time")
    added_by: Optional[str] = Field(default=None, alias="added_by")
    update_time: Optional[int] = Field(default=None, alias="update_time")
    url: Optional[str] = Field(default=None, alias="url")
    tos_path: Optional[str] = Field(default=None, alias="tos_path")
    point_num: Optional[int] = Field(default=None, alias="point_num")
    status: Optional[DocStatus] = Field(default=None, alias="status")
    title: Optional[str] = Field(default=None, alias="title")
    source: Optional[str] = Field(default=None, alias="source")
    total_tokens: Optional[int] = Field(default=None, alias="total_tokens")
    doc_summary_tokens: Optional[int] = Field(default=None, alias="doc_summary_tokens")
    doc_premium_status: Optional[DocPremiumStatus] = Field(default=None, alias="doc_premium_status")
    meta: Optional[str] = Field(default=None, alias="meta")
    labels: Optional[Dict[str, str]] = Field(default=None, alias="labels")
    video_outline: Optional[Dict[str, Any]] = Field(default=None, alias="video_outline")
    audio_outline: Optional[Dict[str, Any]] = Field(default=None, alias="audio_outline")
    statistics: Optional[Dict[str, Any]] = Field(default=None, alias="statistics")
    project: Optional[str] = Field(default="default", alias="project")
    resource_id: Optional[str] = Field(default=None, alias="resource_id")


class ListDocsResult(Model):
    doc_list: Sequence[DocInfo] = Field(default_factory=list, alias="doc_list")
    count: Optional[int] = Field(default=None, alias="count")
    total_num: Optional[int] = Field(default=None, alias="total_num")


class ListDocsResponse(DataApiResponse):
    result: Optional[ListDocsResult] = None

class AddDocResponseData(Model):
    collection_name: Optional[str] = Field(default=None, alias="collection_name")
    resource_id: Optional[str] = Field(default=None, alias="resource_id")
    project: Optional[str] = Field(default=None, alias="project")
    doc_id: Optional[str] = Field(default=None, alias="doc_id")
    task_id: Optional[int] = Field(default=None, alias="task_id")
    dedup_info: Optional[DedupInfo] = Field(default=None, alias="dedup_info")
    more_info: Optional[str] = Field(default=None, alias="more_info")

class AddDocResponse(DataApiResponse):
    result: Optional[AddDocResponseData] = None
