# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
from typing import Mapping, Optional, Union, List
import warnings

from .models.base import CollectionMeta, Model
from .models.doc import DocInfo, ListDocsResponse, AddDocRequest, ListDocsRequest, MetaItem, AddDocV2Request, AddDocResponse
from .models.point import (
    ListPointsResponse,
    PointInfo,
    AddPointRequest,
    UpdatePointRequest,
    ListPointsRequest,
    DeletePointRequest,
    PointAddResponse
)
from .models.search import (
    SearchCollectionRequest,
    SearchKnowledgeResponse,
    SearchResponse,
    SearchKnowledgeRequest,
)


class KnowledgeCollection:
    def __init__(self, client, meta: CollectionMeta):
        self.client = client
        self._meta = meta
        self._meta_payload = meta.model_dump(by_alias=True, exclude_none=True)

    def add_doc(
        self,
        request: Union[AddDocRequest, Mapping[str, object]],
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ):
        warnings.warn("add_doc 已废弃，请使用 add_doc_v2", DeprecationWarning, stacklevel=2)
        req_payload = (
            request.model_dump(by_alias=True, exclude_none=True)  # type: ignore[attr-defined]
            if isinstance(request, Model)
            else dict(request)
        )
        payload = {**self._meta_payload, **req_payload}
        res = self.client.json_exception("AddDoc", {}, json.dumps(payload), headers=headers, timeout=timeout)
        response = AddDocResponse.parse_with(res)
        return response

    def add_doc_v2(
        self,
        request: Union[AddDocV2Request, Mapping[str, object]],
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> AddDocResponse:
        req_payload = (
            request.model_dump(by_alias=True, exclude_none=True)  # type: ignore[attr-defined]
            if isinstance(request, Model)
            else dict(request)
        )
        payload = {**self._meta_payload, **req_payload}
        res = self.client.json_exception("AddDocV2", {}, json.dumps(payload), headers=headers, timeout=timeout)
        response = AddDocResponse.parse_with(res)
        return response

    def delete_doc(
        self,
        doc_id: str,
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ):
        payload = {**self._meta_payload, "doc_id": doc_id}
        res = self.client.json_exception("DeleteDoc", {}, json.dumps(payload), headers=headers, timeout=timeout)
        return res

    def get_doc(
        self,
        doc_id: str,
        *,
        return_token_usage: bool = False,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> DocInfo:
        payload = {**self._meta_payload, "doc_id": doc_id}
        if return_token_usage:
            payload["return_token_usage"] = True
        res = self.client.json_exception("GetDocInfo", {}, json.dumps(payload), headers=headers, timeout=timeout)
        data_obj = res["data"] if isinstance(res, dict) and "data" in res else {}
        if not isinstance(data_obj, dict):
            data_obj = {}
        doc = DocInfo.model_validate(
            {**data_obj, "project": self._meta.project_name or "default", "resource_id": self._meta.resource_id}
        )
        return doc

    def list_docs(
        self,
        request: Union[ListDocsRequest, Mapping[str, object]],
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> ListDocsResponse:
        req_payload = (
            request.model_dump(by_alias=True, exclude_none=True)  # type: ignore[attr-defined]
            if isinstance(request, Model)
            else dict(request)
        )
        payload: dict = {**self._meta_payload, **req_payload}
        res = self.client.json_exception("ListDocs", {}, json.dumps(payload), headers=headers, timeout=timeout)
        response = ListDocsResponse.parse_with(res)
        return response

    def update_doc_meta(
        self,
        doc_id: str,
        meta: List[MetaItem],
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ):
        payload = {**self._meta_payload, "doc_id": doc_id, "meta": [item.model_dump(by_alias=True) for item in meta]}
        res = self.client.json_exception("UpdateDocMeta", {}, json.dumps(payload), headers=headers, timeout=timeout)
        return res

    def update_doc(
        self,
        doc_id: str,
        doc_name: str,
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ):
        payload = {**self._meta_payload, "doc_id": doc_id, "doc_name": doc_name}
        res = self.client.json_exception("UpdateDoc", {}, json.dumps(payload), headers=headers, timeout=timeout)
        return res

    def get_point(
        self,
        point_id: str,
        *,
        get_attachment_link: bool = False,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> PointInfo:
        payload = {**self._meta_payload, "point_id": point_id}
        if get_attachment_link:
            payload["get_attachment_link"] = True
        res = self.client.json_exception("GetPointInfo", {}, json.dumps(payload), headers=headers, timeout=timeout)
        data_obj = res["data"] if isinstance(res, dict) and "data" in res else {}
        if not isinstance(data_obj, dict):
            data_obj = {}
        point = PointInfo.model_validate(
            {**data_obj, "project": self._meta.project_name or "default", "resource_id": self._meta.resource_id}
        )
        return point

    def list_points(
        self,
        request: Union[ListPointsRequest, Mapping[str, object]],
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> ListPointsResponse:
        req_payload = (
            request.model_dump(by_alias=True, exclude_none=True)  # type: ignore[attr-defined]
            if isinstance(request, Model)
            else dict(request)
        )
        payload: dict = {**self._meta_payload, **req_payload}
        res = self.client.json_exception("ListPoints", {}, json.dumps(payload), headers=headers, timeout=timeout)
        response = ListPointsResponse.parse_with(res)
        return response

    def add_point(
        self,
        request: Union[AddPointRequest, Mapping[str, object]],
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ):
        req_payload = (
            request.model_dump(by_alias=True, exclude_none=True)  # type: ignore[attr-defined]
            if isinstance(request, Model)
            else dict(request)
        )
        payload = {**self._meta_payload, **req_payload}
        res = self.client.json_exception("AddPoint", {}, json.dumps(payload), headers=headers, timeout=timeout)
        response = PointAddResponse.parse_with(res)
        return response

    def update_point(
        self,
        point_id: str,
        update: Union[UpdatePointRequest, Mapping[str, object]],
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ):
        upd_payload = (
            update.model_dump(by_alias=True, exclude_none=True)  # type: ignore[attr-defined]
            if isinstance(update, Model)
            else dict(update)
        )
        payload = {**self._meta_payload, "point_id": point_id, **upd_payload}
        res = self.client.json_exception("UpdatePoint", {}, json.dumps(payload), headers=headers, timeout=timeout)
        return res

    def delete_point(
        self,
        request: Union[DeletePointRequest, Mapping[str, object]],
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ):
        req_payload = (
            request.model_dump(by_alias=True, exclude_none=True)  # type: ignore[attr-defined]
            if isinstance(request, Model)
            else dict(request)
        )
        payload = {**self._meta_payload, **req_payload}
        res = self.client.json_exception("DeletePoint", {}, json.dumps(payload), headers=headers, timeout=timeout)
        return res

    def search_collection(
        self,
        request: Union[SearchCollectionRequest, Mapping[str, object]],
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> SearchResponse:
        req_payload = (
            request.model_dump(by_alias=True, exclude_none=True)  # type: ignore[attr-defined]
            if isinstance(request, Model)
            else dict(request)
        )
        payload: dict = {**self._meta_payload, **req_payload, "name": self._meta.collection_name}
        res = self.client.json_exception("SearchCollection", {}, json.dumps(payload), headers=headers, timeout=timeout)
        response = SearchResponse.parse_with(res)
        return response


    def search_knowledge(
        self,
        request: Union[SearchKnowledgeRequest, Mapping[str, object]],
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> SearchKnowledgeResponse:
        req_payload = (
            request.model_dump(by_alias=True, exclude_none=True)  # type: ignore[attr-defined]
            if isinstance(request, Model)
            else dict(request)
        )
        payload: dict = {**self._meta_payload, **req_payload, "name": self._meta.collection_name}
        res = self.client.json_exception("SearchKnowledge", {}, json.dumps(payload), headers=headers, timeout=timeout)
        response = SearchKnowledgeResponse.parse_with(res)
        return response
