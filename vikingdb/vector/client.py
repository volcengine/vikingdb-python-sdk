# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Optional

from volcengine.ApiInfo import ApiInfo

from .._client import Client
from ..auth import Auth
from .exceptions import EXCEPTION_MAP, VikingVectorException
from ..request_options import RequestOptions, ensure_request_options
from ..version import __version__
from .models import CollectionMeta, IndexMeta

if TYPE_CHECKING:
    from .collection import CollectionClient
    from .embedding import EmbeddingClient
    from .index import IndexClient

_REQUEST_ID_HEADER = "X-Tt-Logid"
_DEFAULT_USER_AGENT = f"vikingdb-python-sdk/{__version__}"

API_VECTOR_DATA_UPSERT = "VectorDataUpsert"
API_VECTOR_DATA_UPDATE = "VectorDataUpdate"
API_VECTOR_DATA_DELETE = "VectorDataDelete"
API_VECTOR_DATA_FETCH_IN_COLLECTION = "VectorDataFetchInCollection"
API_VECTOR_DATA_FETCH_IN_INDEX = "VectorDataFetchInIndex"
API_VECTOR_SEARCH_BY_VECTOR = "VectorSearchByVector"
API_VECTOR_SEARCH_BY_MULTI_MODAL = "VectorSearchByMultiModal"
API_VECTOR_SEARCH_BY_ID = "VectorSearchByID"
API_VECTOR_SEARCH_BY_SCALAR = "VectorSearchByScalar"
API_VECTOR_SEARCH_BY_KEYWORDS = "VectorSearchByKeywords"
API_VECTOR_SEARCH_BY_RANDOM = "VectorSearchByRandom"
API_VECTOR_DATA_AGGREGATE = "VectorDataAggregate"
API_VECTOR_EMBEDDING = "VectorEmbedding"


class VikingVector(Client):
    """Unified Vector client combining service and convenience helpers."""

    def __init__(
        self,
        *,
        host: str,
        region: str,
        auth: Auth,
        scheme: str = "https",
        sts_token: str = "",
        timeout: int = 30,
    ) -> None:
        if auth is None:
            raise ValueError("auth is required for VikingVector")

        super().__init__(
            host=host,
            region=region,
            service="vikingdb",
            auth=auth,
            sts_token=sts_token,
            scheme=scheme,
            timeout=timeout,
        )

    def collection(
        self,
        *,
        resource_id: Optional[str] = None,
        collection_name: Optional[str] = None,
        project_name: Optional[str] = None,
    ) -> "CollectionClient":
        from .collection import CollectionClient

        meta = CollectionMeta(
            resource_id=resource_id,
            collection_name=collection_name,
            project_name=project_name,
        )
        return CollectionClient(self, meta)

    def index(
        self,
        *,
        resource_id: Optional[str] = None,
        collection_name: Optional[str] = None,
        project_name: Optional[str] = None,
        index_name: Optional[str] = None,
    ) -> "IndexClient":
        from .index import IndexClient

        meta = IndexMeta(
            resource_id=resource_id,
            collection_name=collection_name,
            project_name=project_name,
            index_name=index_name,
        )
        return IndexClient(self, meta)

    def embedding(self) -> "EmbeddingClient":
        from .embedding import EmbeddingClient

        return EmbeddingClient(self)

    def request(
        self,
        api: str,
        payload: Mapping[str, object],
        *,
        options: Optional[RequestOptions] = None,
    ) -> Mapping[str, object]:
        request_options = ensure_request_options(options)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": _DEFAULT_USER_AGENT,
        }
        if request_options.headers:
            headers.update(request_options.headers)
        if request_options.request_id:
            headers[_REQUEST_ID_HEADER] = request_options.request_id

        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        params = dict(request_options.query) if request_options.query else None
        response_data = self.json_exception(api, params, body, headers=headers, timeout=request_options.timeout)
        if not response_data:
            return {}
        return response_data

    def json_exception(
        self,
        api: str,
        params: Optional[Mapping[str, Any]],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
        *,
        timeout: Optional[int] = None,
    ) -> Any:
        """Send JSON request and raise structured vector exceptions on failure."""
        try:
            response = self._json(api, params, body, headers=headers, timeout=timeout)
        except Exception as e:
            try:
                err_msg = (
                    e.args[0].decode("utf-8")
                    if isinstance(e.args[0], bytes)
                    else str(e.args[0])
                )
                res_json = json.loads(err_msg)
            except:
                raise VikingVectorException(
                    1000028, "missed", "failed to decode error response for {}, res:{}".format(api, str(e))
                ) from None
            if "ResponseMetadata" in res_json:
                error = res_json["ResponseMetadata"].get("Error", {})
                code = error.get("Code", 1000028)
                request_id = error.get("RequestId", "unknown")
                message = error.get("Message", None)
                raise EXCEPTION_MAP.get(code, VikingVectorException)(
                    code, request_id, message
                ) from None
            else:
                code = res_json.get("code", 1000028)
                request_id = res_json.get("request_id", "unknown")
                message = res_json.get("message", None)
                raise VikingVectorException(
                    code, request_id, message
                ) from None
        if response is None:
            raise VikingVectorException(
                1000028, request_id,
                f"empty response received for api {api}",
            ) from None
        return response

    def _build_api_info(self):
        header = {"Accept": "application/json"}
        return {
            API_VECTOR_DATA_UPSERT: ApiInfo(
                "POST",
                "/api/vikingdb/data/upsert",
                {},
                {},
                header,
            ),
            API_VECTOR_DATA_UPDATE: ApiInfo(
                "POST",
                "/api/vikingdb/data/update",
                {},
                {},
                header,
            ),
            API_VECTOR_DATA_DELETE: ApiInfo(
                "POST",
                "/api/vikingdb/data/delete",
                {},
                {},
                header,
            ),
            API_VECTOR_DATA_FETCH_IN_COLLECTION: ApiInfo(
                "POST",
                "/api/vikingdb/data/fetch_in_collection",
                {},
                {},
                header,
            ),
            API_VECTOR_DATA_FETCH_IN_INDEX: ApiInfo(
                "POST",
                "/api/vikingdb/data/fetch_in_index",
                {},
                {},
                header,
            ),
            API_VECTOR_SEARCH_BY_VECTOR: ApiInfo(
                "POST",
                "/api/vikingdb/data/search/vector",
                {},
                {},
                header,
            ),
            API_VECTOR_SEARCH_BY_MULTI_MODAL: ApiInfo(
                "POST",
                "/api/vikingdb/data/search/multi_modal",
                {},
                {},
                header,
            ),
            API_VECTOR_SEARCH_BY_ID: ApiInfo(
                "POST",
                "/api/vikingdb/data/search/id",
                {},
                {},
                header,
            ),
            API_VECTOR_SEARCH_BY_SCALAR: ApiInfo(
                "POST",
                "/api/vikingdb/data/search/scalar",
                {},
                {},
                header,
            ),
            API_VECTOR_SEARCH_BY_KEYWORDS: ApiInfo(
                "POST",
                "/api/vikingdb/data/search/keywords",
                {},
                {},
                header,
            ),
            API_VECTOR_SEARCH_BY_RANDOM: ApiInfo(
                "POST",
                "/api/vikingdb/data/search/random",
                {},
                {},
                header,
            ),
            API_VECTOR_DATA_AGGREGATE: ApiInfo(
                "POST",
                "/api/vikingdb/data/agg",
                {},
                {},
                header,
            ),
            API_VECTOR_EMBEDDING: ApiInfo(
                "POST",
                "/api/vikingdb/embedding",
                {},
                {},
                header,
            ),
        }
