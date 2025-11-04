# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence

from pydantic import Field

from .base import DataApiResponse, Model


class DataItem(Model):
    id: Any = Field(alias="id")
    fields: Dict[str, Any] = Field(default_factory=dict, alias="fields")


class WriteDataBase(Model):
    data: Sequence[Mapping[str, Any]] = Field(alias="data")
    ttl: Optional[int] = Field(default=None, alias="ttl")
    ignore_unknown_fields: Optional[bool] = Field(default=None, alias="ignore_unknown_fields")


class UpsertDataRequest(WriteDataBase):
    async_write: Optional[bool] = Field(default=None, alias="async")


class UpsertDataResult(Model):
    token_usage: Dict[str, Any] = Field(default_factory=dict, alias="token_usage")


class UpdateDataRequest(WriteDataBase):
    pass


class UpdateDataResult(Model):
    token_usage: Dict[str, Any] = Field(default_factory=dict, alias="token_usage")


class DeleteDataRequest(Model):
    ids: Optional[Sequence[Any]] = Field(default=None, alias="ids")
    delete_all: Optional[bool] = Field(default=None, alias="del_all")


class DeleteDataResponse(DataApiResponse):
    pass


class FetchDataInCollectionRequest(Model):
    ids: Sequence[Any] = Field(alias="ids")


class FetchDataInCollectionResult(Model):
    items: List[DataItem] = Field(default_factory=list, alias="fetch")
    ids_not_exist: List[Any] = Field(default_factory=list, alias="ids_not_exist")


class FetchDataInCollectionResponse(DataApiResponse):
    result: Optional[FetchDataInCollectionResult] = None


class UpsertDataResponse(DataApiResponse):
    result: Optional[UpsertDataResult] = None


class UpdateDataResponse(DataApiResponse):
    result: Optional[UpdateDataResult] = None
