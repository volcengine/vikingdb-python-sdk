# coding:utf-8
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

from .client import VikingMemClient
from .collection import Collection
from .auth import AKSKAuthProvider, APIKeyAuthProvider, AuthProvider, create_auth_provider
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
    "VikingMemClient",
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

