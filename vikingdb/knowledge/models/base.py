# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Mapping, Optional, Type, TypeVar

from pydantic import BaseModel, ConfigDict, Field

TModel = TypeVar("TModel", bound="Model")

__all__ = [
    "Model",
    "CollectionMeta",
    "CommonResponse",
    "DataApiResponse",
]


class Model(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=None, extra="allow")


class CollectionMeta(Model):
    collection_name: Optional[str] = Field(default=None, alias="collection_name")
    project_name: Optional[str] = Field(default=None, alias="project")
    resource_id: Optional[str] = Field(default=None, alias="resource_id")


class CommonResponse(Model):
    api: Optional[str] = Field(default=None, alias="api")
    message: Optional[str] = Field(default=None, alias="message")
    code: Optional[str] = Field(default=None, alias="code")
    request_id: Optional[str] = Field(default=None, alias="request_id")


class DataApiResponse(Model):
    code: Optional[int] = Field(default=None, alias="code")
    message: Optional[str] = Field(default=None, alias="message")
    request_id: Optional[str] = Field(default=None, alias="request_id")
    data: Optional[Any] = Field(default=None, alias="data")
    result: Optional[Any] = Field(default=None, alias="result")

    @classmethod
    def parse_with(
        cls,
        payload: Mapping[str, Any],
    ) -> "DataApiResponse":
        adjusted = dict(payload)
        if "result" not in adjusted and "data" in adjusted:
            adjusted["result"] = adjusted["data"]
        return cls.model_validate(adjusted)
