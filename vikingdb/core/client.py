"""
向量库API客户端模块

提供向量库API的核心客户端类，处理认证、请求发送和响应处理。
"""

import json
import time
import urllib.request
import urllib.error
import urllib.parse
from typing import Dict, Any

from version import __version__
from core.exceptions import (
    VectorDBError,
    VectorDBAuthError,
    VectorDBRequestError,
    VectorDBResponseError
)

class VectorDBClient:
    """向量库API客户端类
    
    处理向量库API的认证、请求发送和响应处理。
    
    Attributes:
        api_key (str): API密钥，用于认证
        base_url (str): API的基础URL
        timeout (int): 请求超时时间（秒）
        retry_enabled (bool): 是否启用重试机制
        max_retries (int): 最大重试次数
        retry_initial_delay (float): 初始重试延迟时间（秒）
    """
    
    def __init__(
        self, 
        api_key: str = None, 
        host: str = None,
        timeout: int = 30,
        protocol: str = 'http',
        retry_enabled: bool = False,
        max_retries: int = 3,
        retry_initial_delay: float = 0.5
    ):
        """初始化客户端
        
        Args:
            api_key (str, optional): API密钥，用于认证
            host (str, optional): API的host
            timeout (int, optional): 请求超时时间（秒），默认为30
            retry_enabled (bool, optional): 是否启用重试机制，默认为False
            max_retries (int, optional): 最大重试次数，默认为3
            retry_initial_delay (float, optional): 初始重试延迟时间（秒），默认为0.5
        """
        self.api_key = api_key
        self.base_url = host or "https://api.volcstack.com"  # 假设的基础URL，需要根据实际情况修改
        self.timeout = timeout
        self.retry_enabled = retry_enabled
        self.max_retries = max_retries
        self.retry_initial_delay = retry_initial_delay
    
    def set_api_key(self, api_key: str) -> None:
        """设置API密钥
        
        Args:
            api_key (str): API密钥
        """
        self.api_key = api_key
    
    def enable_retry(self, enabled: bool = True) -> None:
        """启用或禁用重试机制
        
        Args:
            enabled (bool, optional): 是否启用重试，默认为True
        """
        self.retry_enabled = enabled
    
    def configure_retry(self, max_retries: int = None, initial_delay: float = None) -> None:
        """配置重试参数
        
        Args:
            max_retries (int, optional): 最大重试次数
            initial_delay (float, optional): 初始重试延迟时间（秒）
        """
        if max_retries is not None:
            self.max_retries = max_retries
        if initial_delay is not None:
            self.retry_initial_delay = initial_delay
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头
        
        Returns:
            Dict[str, str]: 包含认证和版本信息的请求头
        
        Raises:
            VectorDBAuthError: 如果API密钥未设置
        """
        if not self.api_key:
            raise VectorDBAuthError("API密钥未设置，请使用set_api_key方法设置API密钥")
        
        return {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": f"volcstack-python-sdk/{__version__}",
            "Content-Type": "application/json"
        }
    
    def _calculate_retry_delay(self, retry_count: int) -> float:
        """计算重试延迟时间，使用指数退避算法
        
        Args:
            retry_count (int): 当前重试次数
        
        Returns:
            float: 延迟时间（秒）
        """
        # 指数退避算法：delay = initial_delay * (2^retry_count)
        return self.retry_initial_delay * (2 ** retry_count)
    
    def _send_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Dict[str, Any] = None, 
        data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """发送HTTP请求
        
        Args:
            method (str): HTTP方法，如'GET'、'POST'等
            endpoint (str): API端点路径
            params (Dict[str, Any], optional): URL参数
            data (Dict[str, Any], optional): 请求体数据
        
        Returns:
            Dict[str, Any]: API响应数据
        
        Raises:
            VectorDBRequestError: 请求发送失败
            VectorDBResponseError: 响应解析失败
            VectorDBError: API返回错误
        """
        url = f"{self.base_url}{endpoint}"
        
        # 处理URL参数
        if params:
            query_string = urllib.parse.urlencode(params)
            url = f"{url}?{query_string}"
        
        # 准备请求体
        body = None
        if data:
            body = json.dumps(data).encode('utf-8')
        
        # 创建请求对象
        headers = self._get_headers()
        req = urllib.request.Request(
            url=url,
            data=body,
            headers=headers,
            method=method
        )
        
        retry_count = 0
        while True:
            try:
                # 发送请求
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    response_data = response.read().decode('utf-8')
                    
                    # 解析响应
                    try:
                        result = json.loads(response_data)
                    except json.JSONDecodeError:
                        raise VectorDBResponseError("无法解析API响应")
                    
                    # 检查API错误
                    if result.get('code') != "Success":
                        raise VectorDBError(
                            code=result.get('code'),
                            message=result.get('message'),
                            request_id=result.get('request_id')
                        )
                    
                    return result
                    
            except urllib.error.HTTPError as e:
                # 处理HTTP错误
                try:
                    error_data = json.loads(e.read().decode('utf-8'))
                    
                    # 检查是否为429错误（Too Many Requests）且启用了重试
                    if e.code == 429 and self.retry_enabled and retry_count < self.max_retries:
                        retry_count += 1
                        retry_delay = self._calculate_retry_delay(retry_count)
                        time.sleep(retry_delay)
                        continue
                    
                    raise VectorDBError(
                        code=error_data.get('code'),
                        message=error_data.get('message'),
                        request_id=error_data.get('request_id'),
                        status_code=e.code
                    )
                except json.JSONDecodeError:
                    raise VectorDBRequestError(f"HTTP错误: {e.code} {e.reason}")
            
            except urllib.error.URLError as e:
                # 处理网络错误
                raise VectorDBRequestError(f"网络错误: {str(e.reason)}")
            
            except Exception as e:
                # 处理其他错误
                raise VectorDBRequestError(f"请求错误: {str(e)}")
            
            # 如果没有异常或不需要重试，跳出循环
            break
    
    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送GET请求
        
        Args:
            endpoint (str): API端点路径
            params (Dict[str, Any], optional): URL参数
        
        Returns:
            Dict[str, Any]: API响应数据
        """
        return self._send_request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送POST请求
        
        Args:
            endpoint (str): API端点路径
            data (Dict[str, Any], optional): 请求体数据
            params (Dict[str, Any], optional): URL参数
        
        Returns:
            Dict[str, Any]: API响应数据
        """
        return self._send_request("POST", endpoint, params=params, data=data)
    
    def put(self, endpoint: str, data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送PUT请求
        
        Args:
            endpoint (str): API端点路径
            data (Dict[str, Any], optional): 请求体数据
            params (Dict[str, Any], optional): URL参数
        
        Returns:
            Dict[str, Any]: API响应数据
        """
        return self._send_request("PUT", endpoint, params=params, data=data)
    
    def delete(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送DELETE请求
        
        Args:
            endpoint (str): API端点路径
            params (Dict[str, Any], optional): URL参数
        
        Returns:
            Dict[str, Any]: API响应数据
        """
        return self._send_request("DELETE", endpoint, params=params)
    
    # 示例API方法，实际方法需要根据具体API文档实现
    def create_vector(self, vector_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建向量（示例方法）
        
        Args:
            vector_data (Dict[str, Any]): 向量数据
        
        Returns:
            Dict[str, Any]: API响应数据
        """
        return self.post("/vectors", data=vector_data)
    
    def search_vectors(self, query_vector: Dict[str, Any]) -> Dict[str, Any]:
        """搜索向量（示例方法）
        
        Args:
            query_vector (Dict[str, Any]): 查询向量数据
        
        Returns:
            Dict[str, Any]: API响应数据
        """
        return self.post("/vectors/search", data=query_vector)