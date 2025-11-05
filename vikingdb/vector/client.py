# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
import time
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Optional

from volcengine.ApiInfo import ApiInfo

from .._client import Client, _REQUEST_ID_HEADER
from ..auth import Auth
from ..exceptions import VikingException
from .exceptions import VikingVectorException, VikingConnectionException
from ..request_options import RequestOptions, ensure_request_options
from ..version import __version__
from .models import CollectionMeta, IndexMeta

if TYPE_CHECKING:
    from .collection import CollectionClient
    from .embedding import EmbeddingClient
    from .index import IndexClient

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
        try:
            resp = self.session.get(f"{scheme}://{host}/api/vikingdb/Ping")
            if resp.status_code != 200:
                raise VikingConnectionException(f"failed to ping {host}", f"{resp.status_code}")
        except Exception as exp:
            raise VikingConnectionException(f"failed to ping {host} ", str(exp))

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
        max_attempts = (
            request_options.max_attempts
            if request_options.max_attempts and request_options.max_attempts > 0
            else 3
        )
        initial_delay_seconds = 0.5
        max_delay_seconds = 8.0
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
        for attempt in range(1, max_attempts + 1):
            try:
                response_data = self.json_exception(
                    api,
                    params,
                    body,
                    headers=headers,
                    timeout=request_options.timeout,
                )
                if not response_data:
                    return {}
                return response_data
            except Exception:
                if attempt >= max_attempts:
                    raise
                delay = min(
                    initial_delay_seconds * (2 ** (attempt - 1)),
                    max_delay_seconds,
                )
                time.sleep(delay)

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
        except VikingException as exc:
            raise exc.promote(VikingVectorException) from None
        if response is None:
            raise VikingVectorException(
                "InternalServerError",
                "unknown",
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
