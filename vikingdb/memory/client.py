# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""Viking Memory Service Main Service Class"""

from __future__ import annotations

from volcengine.ApiInfo import ApiInfo

from .._client import Client
from ..auth import Auth
from ..exceptions import VikingException, promote_exception
from .collection import Collection
from .exceptions import EXCEPTION_MAP, VikingMemException
from ..version import __version__
_DEFAULT_USER_AGENT = f"vikingdb-python-sdk/{__version__}"

def _get_common_viking_request_header():
    """Get common request headers"""
    common_header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": _DEFAULT_USER_AGENT,
    }
    return common_header


class VikingMem(Client):
    """Viking Memory Service Main Service Class"""

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
        """
        Initialize Viking Memory Service

        Args:
            host: API host address
            region: Region
            auth: Authentication provider (e.g. IAM or APIKey)
            sts_token: STS Token (optional)
            scheme: Request protocol (http or https)
            timeout: Timeout in seconds applied to connection and read operations
            
        Note:
            Authentication methods:
            - IAM authentication: ``auth=IAM(ak=\"<AK>\", sk=\"<SK>\")``
            - API Key authentication: ``auth=APIKey(api_key=\"<API_KEY>\")``
        """
        super().__init__(
            host=host,
            region=region,
            service="air",
            auth=auth,
            sts_token=sts_token,
            scheme=scheme,
            timeout=timeout,
        )

    def ping(self):
        """
        Test if authentication credentials (IAM or API Key) are correct
        
        This method sends a ping request to verify:
        - Network connectivity to the service
        - Authentication credentials are valid
        - Service is accessible
        
        Returns:
            bool: Returns True if ping is successful
            
        Raises:
            VikingMemException: Raised when authentication fails or service is unreachable
        """
        try:
            # Use parent class's get method for GET requests
            self.get("Ping", {})
            return True
        except Exception as e:
            raise VikingMemException(
                1000028, 
                "missed", 
                "Authentication failed or service unreachable. Please check your IAM or API Key credentials: {}".format(str(e))
            ) from None

    def _build_api_info(self):
        """Get API information"""
        api_info = {
            # Profile APIs
            "AddProfile": ApiInfo(
                "POST",
                "/api/memory/profile/add",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            "DeleteProfile": ApiInfo(
                "POST",
                "/api/memory/profile/delete",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            "BatchDeleteProfile": ApiInfo(
                "POST",
                "/api/memory/profile/batch_delete",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            "UpdateProfile": ApiInfo(
                "POST",
                "/api/memory/profile/update",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            "TriggerUpdateProfile": ApiInfo(
                "POST",
                "/api/memory/profile/trigger_update",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            # Event APIs
            "AddEvent": ApiInfo(
                "POST",
                "/api/memory/event/add",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            "UpdateEvent": ApiInfo(
                "POST",
                "/api/memory/event/update",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            "DeleteEvent": ApiInfo(
                "POST",
                "/api/memory/event/delete",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            "BatchDeleteEvent": ApiInfo(
                "POST",
                "/api/memory/event/batch_delete",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            # Session APIs
            "AddSession": ApiInfo(
                "POST",
                "/api/memory/session/add",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            "GetSessionInfo": ApiInfo(
                "POST",
                "/api/memory/session/info",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            # Search APIs
            "SearchMemory": ApiInfo(
                "POST",
                "/api/memory/search",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            "SearchEventMemory": ApiInfo(
                "POST",
                "/api/memory/event/search",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            "SearchProfileMemory": ApiInfo(
                "POST",
                "/api/memory/profile/search",
                {},
                {},
                _get_common_viking_request_header(),
            ),
            # Service APIs
            "Ping": ApiInfo("GET", "/api/memory/ping", {}, {}, _get_common_viking_request_header()),
        }
        return api_info

    def json_exception(self, api, params, body, headers=None, timeout=None):
        """Send JSON request with exception handling
        
        Args:
            api: API name
            params: Query parameters
            body: Request body
            headers: Additional headers (optional)
            timeout: Timeout in seconds (optional). If not provided, uses default timeout.
        """
        try:
            res = self._json(api, params, body, headers=headers, timeout=timeout)
        except VikingException as exc:
            raise promote_exception(
                exc,
                exception_map=EXCEPTION_MAP,
                default_cls=VikingMemException,
            ) from None
        if res is None:
            raise VikingMemException(
                1000028,
                "missed",
                "empty response due to unknown error, please contact customer service",
            ) from None
        return res


    async def async_json_exception(self, api, params, body, headers=None, timeout=None):
        """Send JSON request asynchronously with exception handling
        
        Args:
            api: API name
            params: Query parameters
            body: Request body
            headers: Additional headers (optional)
            timeout: Timeout in seconds (optional). If not provided, uses default timeout.
        """
        try:
            res = await self.async_json(api, params, body, headers=headers, timeout=timeout)
        except VikingException as exc:
            raise promote_exception(
                exc,
                exception_map=EXCEPTION_MAP,
                default_cls=VikingMemException,
            ) from None
        if res is None:
            raise VikingMemException(
                1000028,
                "missed",
                "empty response due to unknown error, please contact customer service",
            ) from None
        return res

    def get_collection(self, collection_name=None, project_name="default", resource_id=None) -> Collection:
        """
        Get collection information
        
        This method supports two usage patterns:
        1. Using collection_name and project_name: Provide collection_name (required) and optionally 
           project_name (defaults to "default") to identify the collection.
        2. Using resource_id: Provide resource_id directly to identify the collection uniquely.

        Args:
            collection_name (str, optional): The name of the collection. Required when not using resource_id.
            project_name (str, optional): The name of the project. Defaults to "default". 
                                         Only used when collection_name is provided.
            resource_id (str, optional): The unique resource identifier of the collection. 
                                        When provided, collection_name and project_name are ignored.
            
        Returns:
            Collection: A Collection object for interacting with the specified collection.
            
        Raises:
            ValueError: When neither collection_name nor resource_id is provided.
            
        Examples:
            # Method 1: Using collection_name and project_name
            collection = client.get_collection(
                collection_name="my_collection",
                project_name="my_project"
            )
            
            # Method 2: Using resource_id only
            collection = client.get_collection(
                resource_id="col-abc123xyz"
            )
            
        Note:
            Either provide (collection_name + optional project_name) OR resource_id, not both.
            When resource_id is provided, it takes precedence over collection_name/project_name.
        """
        if resource_id is None and collection_name is None:
            raise ValueError(
                "Either 'collection_name' or 'resource_id' must be provided to identify the collection"
            )

        return Collection(self, collection_name, project_name, resource_id)

    
