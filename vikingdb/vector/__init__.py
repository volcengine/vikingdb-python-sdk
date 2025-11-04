# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

from ..config import ClientConfig, DEFAULT_USER_AGENT
from ..credentials import AuthStrategy, IAM
from ..transport import Transport
from .collection import CollectionClient
from .embedding import EmbeddingClient
from .index import IndexClient
from .models import CollectionMeta, IndexMeta, __all__ as _models_all  # noqa: F401
from .models import *  # noqa: F401,F403

__all__ = [
    "CollectionClient",
    "IndexClient",
    "EmbeddingClient",
    "VikingDB",
] + list(_models_all)

del _models_all


class VikingDB:
    """High-level client for VikingDB vector services.

    Instantiate with an authentication strategy (e.g. :class:`~vikingdb.credentials.IAM`
    or :class:`~vikingdb.credentials.APIKey`) and reuse the resulting object to
    create collection, index, or embedding clients.
    """

    def __init__(
        self,
        *,
        endpoint: str,
        auth: AuthStrategy,
        region: str = "cn-beijing",
        timeout: float = 30.0,
        verify_ssl: bool = True,
        user_agent: Optional[str] = None,
    ) -> None:
        if auth is None:
            raise ValueError("auth must be provided")
        if isinstance(auth, IAM):
            auth.configure(region=region)
        config = ClientConfig(
            endpoint=endpoint,
            region=region,
            timeout=timeout,
            verify_ssl=verify_ssl,
            user_agent=user_agent or DEFAULT_USER_AGENT,
        )
        self._transport = Transport(config, auth)

    def collection(
        self,
        *,
        resource_id: Optional[str] = None,
        collection_name: Optional[str] = None,
        project_name: Optional[str] = None,
    ) -> CollectionClient:
        """Return a collection-scoped client sharing this transport."""
        meta = CollectionMeta(
            resource_id=resource_id,
            collection_name=collection_name,
            project_name=project_name,
        )
        return CollectionClient(self._transport, meta)

    def index(
        self,
        *,
        resource_id: Optional[str] = None,
        collection_name: Optional[str] = None,
        project_name: Optional[str] = None,
        index_name: Optional[str] = None,
    ) -> IndexClient:
        """Return an index-scoped client sharing this transport."""
        meta = IndexMeta(
            resource_id=resource_id,
            collection_name=collection_name,
            project_name=project_name,
            index_name=index_name,
        )
        return IndexClient(self._transport, meta)

    def embedding(self) -> EmbeddingClient:
        """Return an embedding client sharing this transport."""
        return EmbeddingClient(self._transport)
