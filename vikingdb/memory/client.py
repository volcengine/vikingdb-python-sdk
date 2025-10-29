# coding:utf-8
"""Viking Memory Service Main Service Class"""

from __future__ import annotations

import json
from typing import List

import aiohttp

from volcengine.ApiInfo import ApiInfo
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

from .auth import create_auth_provider
from .types import EnumEncoder
from .exceptions import EXCEPTION_MAP, VikingMemException
from .collection import Collection


def _get_common_viking_request_header():
    """Get common request headers"""
    common_header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    return common_header


class VikingMemClient(Service):
    """Viking Memory Service Main Service Class"""

    def __init__(
        self,
        host="api-knowledgebase.mlp.cn-beijing.volces.com",
        region="cn-beijing",
        ak="",
        sk="",
        api_key=None,
        auth_provider=None,
        sts_token="",
        scheme="http",
        connection_timeout=30,
        socket_timeout=30,
    ):
        """
        Initialize Viking Memory Service

        Args:
            host: API host address
            region: Region
            ak: Access Key (used with sk, required for AK/SK authentication)
            sk: Secret Key (used with ak, required for AK/SK authentication)
            api_key: API Key (required for API Key authentication, adds api-key field in request headers)
            auth_provider: Custom authentication provider (optional, takes precedence if provided)
            sts_token: STS Token (optional)
            scheme: Request protocol (http or https)
            connection_timeout: Connection timeout in seconds
            socket_timeout: Socket timeout in seconds
            
        Note:
            Authentication methods:
            - AK/SK authentication: Provide ak and sk parameters
            - API Key authentication: Provide api_key parameter
            - Custom authentication: Provide auth_provider parameter
        """
        # Create or use authentication provider
        if auth_provider is None:
            auth_provider = create_auth_provider(ak=ak, sk=sk, api_key=api_key, region=region)
        
        self.auth_provider = auth_provider
        
        # Get credentials (for ServiceInfo)
        credentials = auth_provider.get_credentials()
        
        self.service_info = VikingMemClient.get_service_info(
            host, credentials, scheme, connection_timeout, socket_timeout
        )
        self.api_info = VikingMemClient.get_api_info()
        super(VikingMemClient, self).__init__(self.service_info, self.api_info)

        if sts_token:
            self.set_session_token(session_token=sts_token)

    def ping(self):
        """
        Test if authentication credentials (AK/SK or API Key) are correct
        
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
                "Authentication failed or service unreachable. Please check your AK/SK or API Key: {}".format(str(e))
            ) from None


    def prepare_request(self, api_info, params, doseq=0):
        """
        Override prepare_request method to use standard volcengine signature process
        
        Does not add extra Host, User-Agent headers to keep signature simple
        """
        from volcengine.base.Request import Request
        
        r = Request()
        r.set_shema(self.service_info.scheme)
        r.set_method(api_info.method)
        r.set_host(self.service_info.host)
        r.set_path(api_info.path)
        r.set_connection_timeout(self.service_info.connection_timeout)
        r.set_socket_timeout(self.service_info.socket_timeout)
        r.set_headers(dict(api_info.header))
        
        if params:
            r.set_query(params)
        
        return r

    @staticmethod
    def get_service_info(host, credentials, scheme, connection_timeout, socket_timeout):
        """Get service information"""
        service_info = ServiceInfo(
            host,
            {},
            credentials,
            connection_timeout,
            socket_timeout,
            scheme=scheme,
        )
        return service_info

    @staticmethod
    def get_api_info():
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
            # Service APIs
            "Ping": ApiInfo("GET", "/api/memory/ping", {}, {}, _get_common_viking_request_header()),
        }
        return api_info

    async def async_json(self, api, params, body, headers=None):
        """Send JSON request asynchronously"""
        if not (api in self.api_info):
            raise Exception("no such api")
        api_info = self.api_info[api]
        r = self.prepare_request(api_info, params)
        if headers:
            for key in headers:
                r.headers[key] = headers[key]
        r.headers["Content-Type"] = "application/json"
        r.body = body

        self.auth_provider.sign_request(r)
        timeout = aiohttp.ClientTimeout(
            connect=self.service_info.connection_timeout,
            sock_connect=self.service_info.socket_timeout,
        )
        url = r.build()
        async with aiohttp.request(
            "POST", url, headers=r.headers, data=r.body, timeout=timeout
        ) as r:
            resp = await r.text(encoding="utf-8")
            if r.status == 200:
                return resp
            else:
                raise Exception(resp)

    def json_exception(self, api, params, body, headers=None):
        """Send JSON request with exception handling"""
        try:
            res = self._json(api, params, body, headers=headers)
        except Exception as e:
            try:
                err_msg = (
                    e.args[0].decode("utf-8")
                    if isinstance(e.args[0], bytes)
                    else str(e.args[0])
                )
                res_json = json.loads(err_msg)
            except:
                raise VikingMemException(
                    1000028, "missed", "json load res error, res:{}".format(str(e))
                ) from None
            if "ResponseMetadata" in res_json:
                error = res_json["ResponseMetadata"].get("Error", {})
                code = error.get("Code", 1000028)
                request_id = error.get("RequestId", "unknown")
                message = error.get("Message", None)
                raise EXCEPTION_MAP.get(code, VikingMemException)(
                    code, request_id, message
                ) from None
            else:
                code = res_json.get("code", 1000028)
                request_id = res_json.get("request_id", "unknown")
                message = res_json.get("message", None)
                raise VikingMemException(
                    code, request_id, message
                ) from None
        if res == "":
            raise VikingMemException(
                1000028,
                "missed",
                "empty response due to unknown error, please contact customer service",
            ) from None
        return res

    def _json(self, api, params, body, headers=None):
        """Internal JSON request method"""
        if not (api in self.api_info):
            raise Exception("no such api")
        api_info = self.api_info[api]
        r = self.prepare_request(api_info, params)
        if headers:
            for key in headers:
                r.headers[key] = headers[key]
        r.headers["Content-Type"] = "application/json"
        r.body = body
        self.auth_provider.sign_request(r)
        url = r.build()
        resp = self.session.post(
            url,
            headers=r.headers,
            data=r.body,
            timeout=(
                self.service_info.connection_timeout,
                self.service_info.socket_timeout,
            ),
        )
        if resp.status_code == 200:
            return json.dumps(resp.json())
        else:
            raise Exception(resp.text.encode("utf-8"))

    async def async_json_exception(self, api, params, body, headers=None):
        """Send JSON request asynchronously with exception handling"""
        try:
            res = await self.async_json(api, params, body, headers=headers)
        except Exception as e:
            try:
                err_msg = (
                    e.args[0].decode("utf-8")
                    if isinstance(e.args[0], bytes)
                    else str(e.args[0])
                )
                res_json = json.loads(err_msg)
            except:
                raise VikingMemException(
                    1000028, "missed", "json load res error, res:{}".format(str(e))
                ) from None
            if "ResponseMetadata" in res_json:
                error = res_json["ResponseMetadata"].get("Error", {})
                code = error.get("Code", 1000028)
                request_id = error.get("RequestId", "unknown")
                message = error.get("Message", None)
                raise EXCEPTION_MAP.get(code, VikingMemException)(
                    code, request_id, message
                ) from None
            else:
                code = res_json.get("code", 1000028)
                request_id = res_json.get("request_id", "unknown")
                message = res_json.get("message", None)
                raise VikingMemException(
                    code, request_id, message
                ) from None
        if res == "":
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

    