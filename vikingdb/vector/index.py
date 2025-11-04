# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Mapping, Optional, Union, cast

from ..request_options import RequestOptions
from .base import VectorClientBase
from .models import (
    AggRequest,
    AggResponse,
    DataApiResponse,
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


class IndexClient(VectorClientBase):
    """Client for index-scoped data operations."""

    def __init__(self, transport, meta: IndexMeta) -> None:
        super().__init__(transport)
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
                "/api/vikingdb/data/fetch_in_index",
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
                "/api/vikingdb/data/search/vector",
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
                "/api/vikingdb/data/search/multi_modal",
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
                "/api/vikingdb/data/search/id",
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
                "/api/vikingdb/data/search/scalar",
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
                "/api/vikingdb/data/search/keywords",
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
                "/api/vikingdb/data/search/random",
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
                "/api/vikingdb/data/agg",
                payload,
                AggResponse,
                request_options=request_options,
            ),
        )
        return response
