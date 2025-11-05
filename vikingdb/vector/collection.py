# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Mapping, Optional, Union, cast

from .client import (
    API_VECTOR_DATA_DELETE,
    API_VECTOR_DATA_FETCH_IN_COLLECTION,
    API_VECTOR_DATA_UPDATE,
    API_VECTOR_DATA_UPSERT,
)
from .models import (
    CollectionMeta,
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

if TYPE_CHECKING:
    from .client import VikingVector


class CollectionClient(VectorClientBase):
    """Client for collection-scoped VikingDB data operations."""

    def __init__(self, service: "VikingVector", meta: CollectionMeta) -> None:
        super().__init__(service)
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
                API_VECTOR_DATA_UPSERT,
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
                API_VECTOR_DATA_UPDATE,
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
                API_VECTOR_DATA_DELETE,
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
                API_VECTOR_DATA_FETCH_IN_COLLECTION,
                payload,
                FetchDataInCollectionResponse,
                request_options=request_options,
            ),
        )
        return response
