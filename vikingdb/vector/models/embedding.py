# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from pydantic import Field

from .base import DataApiResponse, Model


class EmbeddingInstruction(Model):
    content: Optional[str] = Field(default=None, alias="content")


class EmbeddingModelOpt(Model):
    name: Optional[str] = Field(default=None, alias="name")
    version: Optional[str] = Field(default=None, alias="version")
    dim: Optional[int] = Field(default=None, alias="dim")
    ndim: Optional[int] = Field(default=None, alias="ndim")
    shape: Optional[Sequence[int]] = Field(default=None, alias="shape")
    instruction: Optional[EmbeddingInstruction] = Field(default=None, alias="instruction")


class FullModalData(Model):
    text: Optional[str] = Field(default=None, alias="text")
    image: Optional[Any] = Field(default=None, alias="image")
    video: Optional[Any] = Field(default=None, alias="video")


class EmbeddingData(Model):
    text: Optional[str] = Field(default=None, alias="text")
    image: Optional[Any] = Field(default=None, alias="image")
    video: Optional[Any] = Field(default=None, alias="video")
    full_modal_seq: Optional[Sequence[FullModalData]] = Field(default=None, alias="full_modal_seq")


class EmbeddingRequest(Model):
    data: Sequence[EmbeddingData] = Field(alias="data")
    dense_model: Optional[EmbeddingModelOpt] = Field(default=None, alias="dense_model")
    sparse_model: Optional[EmbeddingModelOpt] = Field(default=None, alias="sparse_model")
    tensor_model: Optional[EmbeddingModelOpt] = Field(default=None, alias="tensor_model")
    project_name: Optional[str] = Field(default=None, alias="project_name")
    max_retry_time: Optional[int] = Field(default=None, alias="max_retry_time")


class Embedding(Model):
    dense: Optional[List[float]] = Field(default=None, alias="dense")
    sparse: Optional[Dict[str, float]] = Field(default=None, alias="sparse")


class EmbeddingResult(Model):
    data: List[Embedding] = Field(default_factory=list, alias="data")
    token_usage: Dict[str, Any] = Field(default_factory=dict, alias="token_usage")


class EmbeddingResponse(DataApiResponse):
    result: Optional[EmbeddingResult] = None
