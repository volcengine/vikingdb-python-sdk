import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import httpx
from httpx import Limits, Timeout


class BaseHttpClient:
    def __init__(
            self,
            scheme: str = "https",
            host: str = "",
            port: int = None,
            max_connections: int = 10,
            max_retries: int = 3,
            backoff_factor: float = 0.5,
            timeout: int = 10,
    ):
        """
        初始化HTTP客户端

        参数:
            scheme: 请求协议('http'或'https')
            host: API主机名
            port: API端口号
            max_connections: 最大空闲连接数
            max_retries: 最大重试次数
            backoff_factor: 重试退避因子
            timeout: 请求超时时间(秒)
        """
        self.scheme = scheme
        self.host = host
        self.port = port
        self.timeout = timeout

        # 创建httpx客户端
        self.client = httpx.Client(
            limits=Limits(
                max_connections=max_connections,
                max_keepalive_connections=max_connections,
            ),
            timeout=Timeout(timeout),
            transport=httpx.HTTPTransport(
                retries=max_retries,
            )
        )

    def _prepare_url(self, path: str, params: dict = None) -> str:
        """构建完整URL"""
        base = f"{self.scheme}://{self.host}"
        if self.port:
            base += f":{self.port}"
        return base + path

    def request(
            self,
            method: str,
            path: str,
            headers: dict = None,
            params: dict = None,
            body_json: dict = None,
            timeout: int = None,
    ) -> requests.Response:
        """
        发送HTTP请求

        参数:
            method: HTTP方法('GET', 'POST', 'PUT', 'DELETE'等)
            path: 请求路径
            headers: 请求头
            params: 查询参数
            json_data: JSON格式数据
            timeout: 超时时间(覆盖默认值)

        返回:
            requests.Response: 响应对象
        """
        url = self._prepare_url(path)
        actual_timeout = timeout if timeout is not None else self.timeout

        response = self.client.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=body_json,
            timeout=actual_timeout,
        )
        return response

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()