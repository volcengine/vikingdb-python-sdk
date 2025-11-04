# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Mapping, Optional, Type, TypeVar

from pydantic import BaseModel, ConfigDict, Field

TModel = TypeVar("TModel", bound="Model")


__all__ = [
    "Model",
    "CollectionMeta",
    "IndexMeta",
    "CommonResponse",
    "DataApiResponse",
    "PaginationResponse",
]


class Model(BaseModel):
    """Base model enabling alias handling and permissive parsing."""

    model_config = ConfigDict(populate_by_name=True, alias_generator=None, extra="allow")


class CollectionMeta(Model):
    collection_name: Optional[str] = Field(default=None, alias="collection_name")
    project_name: Optional[str] = Field(default=None, alias="project_name")
    resource_id: Optional[str] = Field(default=None, alias="resource_id")


class IndexMeta(CollectionMeta):
    index_name: Optional[str] = Field(default=None, alias="index_name")


class CommonResponse(Model):
    api: Optional[str] = Field(default=None, alias="api")
    message: Optional[str] = Field(default=None, alias="message")
    code: Optional[str] = Field(default=None, alias="code")
    request_id: Optional[str] = Field(default=None, alias="request_id")


class DataApiResponse(Model):
    code: Optional[str] = Field(default=None, alias="code")
    message: Optional[str] = Field(default=None, alias="message")
    request_id: Optional[str] = Field(default=None, alias="request_id")
    api: Optional[str] = Field(default=None, alias="api")
    result: Optional[Any] = None

    @classmethod
    def parse_with(
        cls,
        payload: Mapping[str, Any],
        result_model: Optional[Type[TModel]] = None,
    ) -> "DataApiResponse":
        response = cls.model_validate(payload)
        if result_model is not None and payload.get("result") is not None:
            response.result = result_model.model_validate(payload["result"])  # type: ignore[assignment]
        return response


class PaginationResponse(Model):
    total: Optional[int] = Field(default=None, alias="total")
    page: Optional[int] = Field(default=None, alias="page")
    page_size: Optional[int] = Field(default=None, alias="page_size")
