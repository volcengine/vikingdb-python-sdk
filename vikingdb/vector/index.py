# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Mapping, Optional, Union, cast

from ..request_options import RequestOptions
from .base import VectorClientBase
from .client import (
    API_VECTOR_DATA_AGGREGATE,
    API_VECTOR_DATA_FETCH_IN_INDEX,
    API_VECTOR_SEARCH_BY_ID,
    API_VECTOR_SEARCH_BY_KEYWORDS,
    API_VECTOR_SEARCH_BY_MULTI_MODAL,
    API_VECTOR_SEARCH_BY_RANDOM,
    API_VECTOR_SEARCH_BY_SCALAR,
    API_VECTOR_SEARCH_BY_VECTOR,
)
from .models import (
    AggRequest,
    AggResponse,
    FetchDataInIndexRequest,
    FetchDataInIndexResponse,
    IndexMeta,
    SearchByIDRequest,
    SearchByKeywordsRequest,
    SearchByMultiModalRequest,
    SearchByRandomRequest,
    SearchByScalarRequest,
    SearchByVectorRequest,
    SearchResponse,
)

if TYPE_CHECKING:
    from .client import VikingVector


class IndexClient(VectorClientBase):
    """Client for index-scoped data operations."""

    def __init__(self, service: "VikingVector", meta: IndexMeta) -> None:
        super().__init__(service)
        self._meta = meta
        self._meta_payload = meta.model_dump(by_alias=True, exclude_none=True)

    def fetch(
        self,
        request: Union[FetchDataInIndexRequest, Mapping[str, object]],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> FetchDataInIndexResponse:
        payload = self._merge_payload(self._meta_payload, request)
        response = cast(
            FetchDataInIndexResponse,
            self._post(
                API_VECTOR_DATA_FETCH_IN_INDEX,
                payload,
                FetchDataInIndexResponse,
                request_options=request_options,
            ),
        )
        return response

    def search_by_vector(
        self,
        request: Union[SearchByVectorRequest, Mapping[str, object]],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> SearchResponse:
        payload = self._merge_payload(self._meta_payload, request)
        response = cast(
            SearchResponse,
            self._post(
                API_VECTOR_SEARCH_BY_VECTOR,
                payload,
                SearchResponse,
                request_options=request_options,
            ),
        )
        return response

    def search_by_multi_modal(
        self,
        request: Union[SearchByMultiModalRequest, Mapping[str, object]],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> SearchResponse:
        payload = self._merge_payload(self._meta_payload, request)
        response = cast(
            SearchResponse,
            self._post(
                API_VECTOR_SEARCH_BY_MULTI_MODAL,
                payload,
                SearchResponse,
                request_options=request_options,
            ),
        )
        return response

    def search_by_id(
        self,
        request: Union[SearchByIDRequest, Mapping[str, object]],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> SearchResponse:
        payload = self._merge_payload(self._meta_payload, request)
        response = cast(
            SearchResponse,
            self._post(
                API_VECTOR_SEARCH_BY_ID,
                payload,
                SearchResponse,
                request_options=request_options,
            ),
        )
        return response

    def search_by_scalar(
        self,
        request: Union[SearchByScalarRequest, Mapping[str, object]],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> SearchResponse:
        payload = self._merge_payload(self._meta_payload, request)
        response = cast(
            SearchResponse,
            self._post(
                API_VECTOR_SEARCH_BY_SCALAR,
                payload,
                SearchResponse,
                request_options=request_options,
            ),
        )
        return response

    def search_by_keywords(
        self,
        request: Union[SearchByKeywordsRequest, Mapping[str, object]],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> SearchResponse:
        payload = self._merge_payload(self._meta_payload, request)
        response = cast(
            SearchResponse,
            self._post(
                API_VECTOR_SEARCH_BY_KEYWORDS,
                payload,
                SearchResponse,
                request_options=request_options,
            ),
        )
        return response

    def search_by_random(
        self,
        request: Union[SearchByRandomRequest, Mapping[str, object], None] = None,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> SearchResponse:
        payload = self._merge_payload(self._meta_payload, request)
        response = cast(
            SearchResponse,
            self._post(
                API_VECTOR_SEARCH_BY_RANDOM,
                payload,
                SearchResponse,
                request_options=request_options,
            ),
        )
        return response

    def aggregate(
        self,
        request: Union[AggRequest, Mapping[str, object]],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> AggResponse:
        payload = self._merge_payload(self._meta_payload, request)
        response = cast(
            AggResponse,
            self._post(
                API_VECTOR_DATA_AGGREGATE,
                payload,
                AggResponse,
                request_options=request_options,
            ),
        )
        return response
