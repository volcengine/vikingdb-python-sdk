# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

from ..exceptions import VikingException

__all__ = [
    "VikingKnowledgeException",
    "UnauthorizedException",
    "NoPermissionException",
    "InvalidRequestException",
    "CollectionExistException",
    "CollectionNotExistException",
    "OperationNotAllowedException",
    "IndexExistException",
    "IndexNotExistException",
    "QueryOpFailedException",
    "DataNotFoundException",
    "DelOpFailedException",
    "UpsertOpFailedException",
    "TokenMismatchException",
    "InvalidQueryVecException",
    "InvalidPrimaryKeyException",
    "InvalidPartitionException",
    "InvalidScalarCondException",
    "InvalidProxyServiceException",
    "IndexRecallException",
    "IndexFetchDataException",
    "IndexNotReadyException",
    "APINotImplementedException",
    "CalcEmbeddingFailedException",
    "ListEmbeddingModelsException",
    "InternalServerException",
    "QuotaLimiterException",
    "RerankException",
    "DocNotExistException",
    "DocIsFullException",
    "PointNotExistException",
    "EXCEPTION_MAP",
]


class VikingKnowledgeException(VikingException):
    def __init__(
        self,
        code: int,
        request_id: str,
        message: Optional[str] = None,
        *,
        status_code: Optional[int] = None,
    ):
        if message is None:
            message = f"unknown error, request_id: {request_id}"
        super().__init__(code, request_id, message, status_code=status_code)


class UnauthorizedException(VikingKnowledgeException):
    pass


class NoPermissionException(VikingKnowledgeException):
    pass


class InvalidRequestException(VikingKnowledgeException):
    pass


class CollectionExistException(VikingKnowledgeException):
    pass


class CollectionNotExistException(VikingKnowledgeException):
    pass


class OperationNotAllowedException(VikingKnowledgeException):
    pass


class IndexExistException(VikingKnowledgeException):
    pass


class IndexNotExistException(VikingKnowledgeException):
    pass


class QueryOpFailedException(VikingKnowledgeException):
    pass


class DataNotFoundException(VikingKnowledgeException):
    pass


class DelOpFailedException(VikingKnowledgeException):
    pass


class UpsertOpFailedException(VikingKnowledgeException):
    pass


class TokenMismatchException(VikingKnowledgeException):
    pass


class InvalidQueryVecException(VikingKnowledgeException):
    pass


class InvalidPrimaryKeyException(VikingKnowledgeException):
    pass


class InvalidPartitionException(VikingKnowledgeException):
    pass


class InvalidScalarCondException(VikingKnowledgeException):
    pass


class InvalidProxyServiceException(VikingKnowledgeException):
    pass


class IndexRecallException(VikingKnowledgeException):
    pass


class IndexFetchDataException(VikingKnowledgeException):
    pass


class IndexNotReadyException(VikingKnowledgeException):
    pass


class APINotImplementedException(VikingKnowledgeException):
    pass


class CalcEmbeddingFailedException(VikingKnowledgeException):
    pass


class ListEmbeddingModelsException(VikingKnowledgeException):
    pass


class InternalServerException(VikingKnowledgeException):
    pass


class QuotaLimiterException(VikingKnowledgeException):
    pass


class RerankException(VikingKnowledgeException):
    pass


class DocNotExistException(VikingKnowledgeException):
    pass


class DocIsFullException(VikingKnowledgeException):
    pass


class PointNotExistException(VikingKnowledgeException):
    pass


EXCEPTION_MAP = {
    1000001: UnauthorizedException,
    1000002: NoPermissionException,
    1000003: InvalidRequestException,
    1000004: CollectionExistException,
    1000005: CollectionNotExistException,
    1000006: OperationNotAllowedException,
    1000007: IndexExistException,
    1000008: IndexNotExistException,
    1000010: QueryOpFailedException,
    1000011: DataNotFoundException,
    1000013: DelOpFailedException,
    1000014: UpsertOpFailedException,
    1000015: TokenMismatchException,
    1000016: InvalidQueryVecException,
    1000017: InvalidPrimaryKeyException,
    1000018: InvalidPartitionException,
    1000019: InvalidScalarCondException,
    1000020: InvalidProxyServiceException,
    1000021: IndexRecallException,
    1000022: IndexFetchDataException,
    1000023: IndexNotReadyException,
    1000024: APINotImplementedException,
    1000025: CalcEmbeddingFailedException,
    1000026: ListEmbeddingModelsException,
    1000028: InternalServerException,
    1000029: QuotaLimiterException,
    1000030: RerankException,
    1001001: DocNotExistException,
    1001010: DocIsFullException,
    1002001: PointNotExistException,
}
