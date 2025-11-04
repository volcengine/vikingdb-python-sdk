# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Mapping, Optional, Union, cast

from .models import (
    CollectionMeta,
    DataApiResponse,
    DeleteDataRequest,
    DeleteDataResponse,
    FetchDataInCollectionRequest,
    FetchDataInCollectionResponse,
    UpsertDataRequest,
    UpsertDataResponse,
    UpdateDataRequest,
    UpdateDataResponse,
)
from ..request_options import RequestOptions
from .base import VectorClientBase


class CollectionClient(VectorClientBase):
    """Client for collection-scoped VikingDB data operations."""

    def __init__(self, transport, meta: CollectionMeta) -> None:
        super().__init__(transport)
        self._meta = meta
        self._meta_payload = meta.model_dump(by_alias=True, exclude_none=True)

    def upsert(
        self,
        request: Union[UpsertDataRequest, Mapping[str, object]],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> UpsertDataResponse:
        payload = self._merge_payload(self._meta_payload, request)
        response = cast(
            UpsertDataResponse,
            self._post(
                "/api/vikingdb/data/upsert",
                payload,
                UpsertDataResponse,
                request_options=request_options,
            ),
        )
        return response

    def update(
        self,
        request: Union[UpdateDataRequest, Mapping[str, object]],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> UpdateDataResponse:
        payload = self._merge_payload(self._meta_payload, request)
        response = cast(
            UpdateDataResponse,
            self._post(
                "/api/vikingdb/data/update",
                payload,
                UpdateDataResponse,
                request_options=request_options,
            ),
        )
        return response

    def delete(
        self,
        request: Union[DeleteDataRequest, Mapping[str, object]],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> DeleteDataResponse:
        payload = self._merge_payload(self._meta_payload, request)
        response = cast(
            DeleteDataResponse,
            self._post(
                "/api/vikingdb/data/delete",
                payload,
                DeleteDataResponse,
                request_options=request_options,
            ),
        )
        return response

    def fetch(
        self,
        request: Union[FetchDataInCollectionRequest, Mapping[str, object]],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> FetchDataInCollectionResponse:
        payload = self._merge_payload(self._meta_payload, request)
        response = cast(
            FetchDataInCollectionResponse,
            self._post(
                "/api/vikingdb/data/fetch_in_collection",
                payload,
                FetchDataInCollectionResponse,
                request_options=request_options,
            ),
        )
        return response
