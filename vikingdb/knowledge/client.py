# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
from typing import Mapping, Optional, Union, Sequence, cast

from volcengine.ApiInfo import ApiInfo

from .. import APIKey
from .._client import Client, _REQUEST_ID_HEADER
from ..auth import Auth
from ..exceptions import VikingException, promote_exception
from .exceptions import EXCEPTION_MAP, VikingKnowledgeException
from ..version import __version__
from .models.base import CollectionMeta, Model
from .models.rerank import RerankDataItem, RerankResponse
from .models.chat import ChatCompletionRequest, ChatCompletionResponse
from .models.service_chat import ServiceChatRequest, ServiceChatResponse


_DEFAULT_USER_AGENT = f"vikingdb-python-sdk/{__version__}"


def _get_common_viking_request_header():
    header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": _DEFAULT_USER_AGENT,
    }
    return header


class VikingKnowledge(Client):
    def __init__(
        self,
        *,
        host: str = "api-knowledgebase.mlp.cn-beijing.volces.com",
        region: str = "cn-beijing",
        auth: Auth,
        sts_token: str = "",
        scheme: str = "http",
        timeout: int = 30,
    ):
        super().__init__(
            host=host,
            region=region,
            service="air",
            auth=auth,
            sts_token=sts_token,
            scheme=scheme,
            timeout=timeout,
        )

    def _build_api_info(self):
        header = _get_common_viking_request_header()
        return {
            "SearchCollection": ApiInfo("POST", "/api/knowledge/collection/search", {}, {}, header),
            "SearchKnowledge": ApiInfo("POST", "/api/knowledge/collection/search_knowledge", {}, {}, header),
            "ServiceChat": ApiInfo("POST", "/api/knowledge/service/chat", {}, {}, header),
            # Doc
            "AddDoc": ApiInfo("POST", "/api/knowledge/doc/add", {}, {}, header),
            "AddDocV2": ApiInfo("POST", "/api/knowledge/doc/v2/add", {}, {}, header),
            "DeleteDoc": ApiInfo("POST", "/api/knowledge/doc/delete", {}, {}, header),
            "GetDocInfo": ApiInfo("POST", "/api/knowledge/doc/info", {}, {}, header),
            "ListDocs": ApiInfo("POST", "/api/knowledge/doc/list", {}, {}, header),
            "UpdateDocMeta": ApiInfo("POST", "/api/knowledge/doc/update_meta", {}, {}, header),
            "UpdateDoc": ApiInfo("POST", "/api/knowledge/doc/update", {}, {}, header),
            # Point
            "GetPointInfo": ApiInfo("POST", "/api/knowledge/point/info", {}, {}, header),
            "ListPoints": ApiInfo("POST", "/api/knowledge/point/list", {}, {}, header),
            "AddPoint": ApiInfo("POST", "/api/knowledge/point/add", {}, {}, header),
            "UpdatePoint": ApiInfo("POST", "/api/knowledge/point/update", {}, {}, header),
            "DeletePoint": ApiInfo("POST", "/api/knowledge/point/delete", {}, {}, header),
            # Service
            "Ping": ApiInfo("GET", "/ping", {}, {}, header),
            "Rerank": ApiInfo("POST", "/api/knowledge/service/rerank", {}, {}, header),
            # Chat
            "ChatCompletion": ApiInfo("POST", "/api/knowledge/chat/completions", {}, {}, header),
        }

    def json_exception(self, api, params, body, headers=None, timeout=None):
        try:
            res = self._json(api, params, body, headers=headers, timeout=timeout)
        except VikingException as exc:
            raise promote_exception(exc, exception_map=EXCEPTION_MAP, default_cls=VikingKnowledgeException) from None
        if res is None:
            raise VikingKnowledgeException(1000028, "missed", "empty response due to unknown error", status_code=None)
        return res

    async def async_json_exception(self, api, params, body, headers=None, timeout=None):
        try:
            res = await self.async_json(api, params, body, headers=headers, timeout=timeout)
        except VikingException as exc:
            raise promote_exception(exc, exception_map=EXCEPTION_MAP, default_cls=VikingKnowledgeException) from None
        if res is None:
            raise VikingKnowledgeException(1000028, "missed", "empty response due to unknown error", status_code=None)
        return res

    def collection(
        self,
        *,
        resource_id: Optional[str] = None,
        collection_name: Optional[str] = None,
        project_name: Optional[str] = None,
    ):
        from .collection import KnowledgeCollection

        meta = CollectionMeta(
            resource_id=resource_id,
            collection_name=collection_name,
            project_name=project_name,
        )
        return KnowledgeCollection(self, meta)

    def rerank(
        self,
        datas: Sequence[Union[RerankDataItem,Mapping[str, object]]],
        *,
        rerank_model: str = "Doubao-pro-4k-rerank",
        rerank_instruction: Optional[str] = None,
        endpoint_id: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> RerankResponse:
        items = [
            (d.model_dump(by_alias=True, exclude_none=True) if isinstance(d, RerankDataItem) else dict(d))
            for d in datas
        ]
        if len(items) > 50:
            raise VikingKnowledgeException(1000028, "missed", "datas list too large", status_code=None)
        payload: dict = {"datas": items, "rerank_model": rerank_model}
        if rerank_instruction is not None:
            payload["rerank_instruction"] = rerank_instruction
        if endpoint_id is not None:
            payload["endpoint_id"] = endpoint_id
        res = self.json_exception("Rerank", {}, json.dumps(payload), headers=headers, timeout=timeout)
        response = RerankResponse.parse_with(res)
        return response

    def chat_completion(
        self,
        request: Union[ChatCompletionRequest, Mapping[str, object]],
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> ChatCompletionResponse:
        payload = (
            request.model_dump(by_alias=True, exclude_none=True)  # type: ignore[attr-defined]
            if isinstance(request, ChatCompletionRequest)
            else dict(request)
        )
        res = self.json_exception("ChatCompletion", {}, json.dumps(payload), headers=headers, timeout=timeout)
        response = ChatCompletionResponse.parse_with(res)
        return response

    def service_chat(
        self,
        request: Union[ServiceChatRequest, Mapping[str, object]],
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> ServiceChatResponse:
        payload = (
            request.model_dump(by_alias=True, exclude_none=True)  # type: ignore[attr-defined]
            if isinstance(request, ServiceChatRequest)
            else dict(request)
        )
        req_headers = dict(headers or {})
        res = self.json_exception("ServiceChat", {}, json.dumps(payload), headers=req_headers, timeout=timeout)
        response = ServiceChatResponse.parse_with(res)
        return response
