# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .auth import APIKey, IAM
from .request_options import RequestOptions
from . import vector
from . import memory
from .vector import (
    CollectionClient,
    EmbeddingClient,
    IndexClient,
    RerankClient,
    VikingDB,
    VikingVector,
)
from .memory import (
    VikingMem,
    Collection,
)
from .knowledge import (
    VikingKnowledge,
    KnowledgeCollection,
)

from .version import __version__
__all__ = [
    "IAM",
    "APIKey",
    "CollectionClient",
    "EmbeddingClient",
    "RerankClient",
    "IndexClient",
    "RequestOptions",
    "VikingDB",
    "VikingVector",
    "vector",
    "memory",
    "VikingMem",
    "Collection",
    "VikingKnowledge",
    "KnowledgeCollection",
    "__version__",
]
