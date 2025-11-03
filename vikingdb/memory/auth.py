# coding:utf-8
"""
Viking Memory Authentication Module

Supports multiple authentication methods:
- AK/SK signature authentication: Uses the standard volcengine SignerV4 signature algorithm
- API Key authentication: Adds api-key field in request headers
"""

from abc import ABC, abstractmethod
from volcengine.Credentials import Credentials
from volcengine.auth.SignerV4 import SignerV4


class AuthProvider(ABC):
    """Base class for authentication providers"""
    
    @abstractmethod
    def sign_request(self, request):
        """
        Sign the request
        
        Args:
            request: volcengine.base.Request object
        """
        pass
    
    @abstractmethod
    def get_credentials(self):
        """
        Get credential information
        
        Returns:
            Credential object or None
        """
        pass


class AKSKAuthProvider(AuthProvider):
    """
    AK/SK signature authentication provider
    
    Uses the standard volcengine SignerV4 signature algorithm
    """
    
    def __init__(self, ak, sk, service="air", region="cn-beijing"):
        """
        Initialize AK/SK authentication
        
        Args:
            ak: Access Key
            sk: Secret Key
            service: Service name, defaults to "air"
            region: Region, defaults to "cn-beijing"
        """
        self.ak = ak
        self.sk = sk
        self.service = service
        self.region = region
        self._credentials = Credentials(ak, sk, service, region)
    
    def sign_request(self, request):
        """Sign the request using SignerV4"""
        SignerV4.sign(request, self._credentials)
    
    def get_credentials(self):
        """Return Credentials object"""
        return self._credentials


class APIKeyAuthProvider(AuthProvider):
    """
    API Key authentication provider
    
    Supports simple API Key authentication by adding api-key field in request headers
    
    Note:
        Reserved feature, not fully implemented yet
    """
    
    def __init__(self, api_key):
        """
        Initialize API Key authentication
        
        Args:
            api_key: API key
        """
        self.api_key = api_key
    
    def sign_request(self, request):
        """
        Sign the request using API Key
        
        Adds api-key field to request headers
        
        Args:
            request: volcengine.base.Request object or similar request object
            
        Note:
            Reserved feature, not implemented yet
        """
        # TODO: API Key authentication feature to be implemented
        # if not hasattr(request, 'headers'):
        #     request.headers = {}
        # request.headers['api-key'] = self.api_key
        pass
    
    def get_credentials(self):
        """API Key method does not use Credentials"""
        return None


def create_auth_provider(ak=None, sk=None, api_key=None, region="cn-beijing", service="air"):
    """
    Factory method: Create appropriate authentication provider based on parameters
    
    Args:
        ak: Access Key
        sk: Secret Key
        api_key: API Key
        region: Region
        service: Service name
    
    Returns:
        AuthProvider: Authentication provider instance
    
    Raises:
        ValueError: When no authentication credentials are provided
    
    Examples:
        # AK/SK authentication
        auth = create_auth_provider(ak="your-ak", sk="your-sk")
        
        # API Key authentication
        auth = create_auth_provider(api_key="your-api-key")
    """
    if ak and sk:
        return AKSKAuthProvider(ak, sk, service, region)
    elif api_key:
        return APIKeyAuthProvider(api_key)
    else:
        raise ValueError(
            "Authentication credentials required: ak+sk or api_key"
        )

