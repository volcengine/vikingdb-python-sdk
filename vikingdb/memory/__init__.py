# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Viking Memory SDK

Provides memory management features including:
- Collection management (create, delete, update, query)
- Profile management (add, delete, update)
- Event management (add, update, delete, batch delete)
- Session management (add messages)
- Memory search (semantic search)

All APIs return plain dictionaries (dict) or lists of dictionaries (list[dict]) without object encapsulation.

Authentication support:
- AK/SK signature authentication (standard volcengine SignerV4)
- API Key authentication (reserved interface)
"""

from .client import VikingMem
from .collection import Collection
from .exceptions import (
    VikingMemException,
    UnauthorizedException,
    InvalidRequestException,
    CollectionExistException,
    CollectionNotExistException,
    IndexExistException,
    IndexNotExistException,
    DataNotFoundException,
    DelOpFailedException,
    UpsertOpFailedException,
    InvalidVectorException,
    InvalidPrimaryKeyException,
    InvalidFilterException,
    IndexSearchException,
    IndexFetchException,
    IndexInitializingException,
    EmbeddingException,
    InternalServerException,
    QuotaLimiterException,
)

__all__ = [
    # Main client classes
    "VikingMem",
    "Collection",
    # Exception classes
    "VikingMemException",
    "UnauthorizedException",
    "InvalidRequestException",
    "CollectionExistException",
    "CollectionNotExistException",
    "IndexExistException",
    "IndexNotExistException",
    "DataNotFoundException",
    "DelOpFailedException",
    "UpsertOpFailedException",
    "InvalidVectorException",
    "InvalidPrimaryKeyException",
    "InvalidFilterException",
    "IndexSearchException",
    "IndexFetchException",
    "IndexInitializingException",
    "EmbeddingException",
    "InternalServerException",
    "QuotaLimiterException",
]
