# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""Viking Memory SDK Exception Definitions"""

from typing import Optional

from ..exceptions import VikingException


class VikingMemException(VikingException):
    """Viking Memory base exception class"""

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
        super().__init__(
            code,
            request_id,
            message,
            status_code=status_code,
        )


class UnauthorizedException(VikingMemException):
    """
    User authentication failed exception (Error code: 1000001)
    
    Triggered by:
    - Incorrect AK/SK configuration
    - Request body not signed
    - Insufficient sub-account permissions
    
    Resolution:
    - Check if AK/SK input is correct
    - Check if request body is signed and signature is added to request headers
    - If sub-account lacks permissions, refer to documentation to request permissions
    """
    pass


class InvalidRequestException(VikingMemException):
    """
    Invalid request parameters exception (Error code: 1000003)
    
    Triggered by:
    - Incorrect request parameter format or incorrect usage
    
    Resolution:
    - Check request parameters based on error message
    """
    pass


class CollectionExistException(VikingMemException):
    """
    Collection already exists exception (Error code: 1000004)
    
    Triggered by:
    - Creating a collection with duplicate name
    
    Resolution:
    - Check if collection exists
    """
    pass


class CollectionNotExistException(VikingMemException):
    """
    Collection does not exist exception (Error code: 1000005)
    
    Triggered by:
    - Collection name is incorrect or does not exist
    
    Resolution:
    - Check if collection exists
    """
    pass


class IndexExistException(VikingMemException):
    """
    Index already exists exception (Error code: 1000007)
    
    Triggered by:
    - Creating an index with duplicate name under the same collection
    
    Resolution:
    - Check if index exists
    """
    pass


class IndexNotExistException(VikingMemException):
    """
    Index does not exist exception (Error code: 1000008)
    
    Triggered by:
    - Index name is incorrect or does not exist
    
    Resolution:
    - Check if index exists
    """
    pass


class DataNotFoundException(VikingMemException):
    """
    Data not found exception (Error code: 1000011)
    
    Triggered by:
    - Attempting to update_data on non-existent data
    
    Resolution:
    - Check if data exists
    """
    pass


class DelOpFailedException(VikingMemException):
    """
    Delete operation failed exception (Error code: 1000013)
    
    Triggered by:
    - Delete operation fails, usually due to server issues
    
    Resolution:
    - Contact customer service promptly
    """
    pass


class UpsertOpFailedException(VikingMemException):
    """
    Upsert operation failed exception (Error code: 1000014)
    
    Triggered by:
    - Upsert operation fails, usually due to server issues
    
    Resolution:
    - Contact customer service promptly
    """
    pass


class InvalidVectorException(VikingMemException):
    """
    Invalid vector exception (Error code: 1000016)
    
    Triggered by:
    - Vector input issues, inconsistent dimensions or incorrect format
    
    Resolution:
    - Check the vector field in the search request
    """
    pass


class InvalidPrimaryKeyException(VikingMemException):
    """
    Invalid primary key exception (Error code: 1000017)
    
    Triggered by:
    - Primary key type mismatch or incorrect format
    
    Resolution:
    - Check the primary key field
    """
    pass


class InvalidFilterException(VikingMemException):
    """
    Invalid scalar filter statement exception (Error code: 1000019)
    
    Triggered by:
    - Incorrect filter format
    - Field not added to scalar index
    - Improper use of field filter statement
    
    Resolution:
    - Check filter statement format and field configuration
    """
    pass


class IndexSearchException(VikingMemException):
    """
    Index search exception (Error code: 1000021)
    
    Triggered by:
    - Server encountered unknown error or failure
    
    Resolution:
    - Contact customer service promptly
    """
    pass


class IndexFetchException(VikingMemException):
    """
    Index fetch data exception (Error code: 1000022)
    
    Triggered by:
    - Server encountered unknown error or failure
    
    Resolution:
    - Contact customer service promptly
    """
    pass


class IndexInitializingException(VikingMemException):
    """
    Index initializing exception (Error code: 1000023)
    
    Triggered by:
    - Attempting to search or query data while index is initializing
    
    Resolution:
    - Wait for index to be ready
    - If not ready after long time (over 1 hour), contact customer service promptly
    """
    pass


class EmbeddingException(VikingMemException):
    """
    Embedding execution exception (Error code: 1000025)
    
    Triggered by:
    - Server error during vectorization of unstructured data
    
    Resolution:
    - If error occurs occasionally, check if input data format is valid
    - Otherwise, contact customer service promptly
    """
    pass


class InternalServerException(VikingMemException):
    """
    Internal server error exception (Error code: 1000028)
    
    Triggered by:
    - Server encountered unexpected error
    
    Resolution:
    - Contact customer service promptly
    """
    pass


class QuotaLimiterException(VikingMemException):
    """
    Request rate limit exceeded exception (Error code: 1000029)
    
    Triggered by:
    - API request QPS too high
    
    Resolution:
    - If search requests are rate limited, increase CPU Quota
    - If other APIs are rate limited, check if calling method has issues
    - Adjust API calling frequency
    """
    pass


# Error code to exception class mapping
EXCEPTION_MAP = {
    1000001: UnauthorizedException,           # User authentication failed
    1000003: InvalidRequestException,         # Invalid request parameters
    1000004: CollectionExistException,        # Collection already exists
    1000005: CollectionNotExistException,     # Collection does not exist
    1000007: IndexExistException,             # Index already exists
    1000008: IndexNotExistException,          # Index does not exist
    1000011: DataNotFoundException,           # Data not found
    1000013: DelOpFailedException,            # Delete operation failed
    1000014: UpsertOpFailedException,         # Upsert operation failed
    1000016: InvalidVectorException,          # Invalid vector
    1000017: InvalidPrimaryKeyException,      # Invalid primary key
    1000019: InvalidFilterException,          # Invalid scalar filter statement
    1000021: IndexSearchException,            # Index search exception
    1000022: IndexFetchException,             # Index fetch data exception
    1000023: IndexInitializingException,      # Index initializing
    1000025: EmbeddingException,              # Embedding execution exception
    1000028: InternalServerException,         # Internal server error
    1000029: QuotaLimiterException,           # Request rate limit exceeded
}
