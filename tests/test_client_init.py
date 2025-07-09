"""
测试客户端初始化和配置
"""

import unittest

from vikingdb.core.client import VectorDBClient
from core.exceptions import VectorDBAuthError


class TestClientInitialization(unittest.TestCase):
    """测试客户端初始化和配置"""

    def test_default_initialization(self):
        """测试默认初始化"""
        client = VectorDBClient()
        self.assertIsNone(client.api_key)
        self.assertEqual(client.base_url, "https://api.volcstack.com")
        self.assertEqual(client.timeout, 30)
        self.assertFalse(client.retry_enabled)
        self.assertEqual(client.max_retries, 3)
        self.assertEqual(client.retry_initial_delay, 0.5)

    def test_custom_initialization(self):
        """测试自定义参数初始化"""
        client = VectorDBClient(
            api_key="test_api_key",
            host="https://custom-api.volcstack.com",
            timeout=60,
            retry_enabled=True,
            max_retries=5,
            retry_initial_delay=1.0
        )
        self.assertEqual(client.api_key, "test_api_key")
        self.assertEqual(client.base_url, "https://custom-api.volcstack.com")
        self.assertEqual(client.timeout, 60)
        self.assertTrue(client.retry_enabled)
        self.assertEqual(client.max_retries, 5)
        self.assertEqual(client.retry_initial_delay, 1.0)

    def test_set_api_key(self):
        """测试设置API密钥"""
        client = VectorDBClient()
        self.assertIsNone(client.api_key)
        
        client.set_api_key("new_api_key")
        self.assertEqual(client.api_key, "new_api_key")

    def test_enable_retry(self):
        """测试启用和禁用重试机制"""
        client = VectorDBClient()
        self.assertFalse(client.retry_enabled)
        
        client.enable_retry(True)
        self.assertTrue(client.retry_enabled)
        
        client.enable_retry(False)
        self.assertFalse(client.retry_enabled)

    def test_configure_retry(self):
        """测试配置重试参数"""
        client = VectorDBClient()
        self.assertEqual(client.max_retries, 3)
        self.assertEqual(client.retry_initial_delay, 0.5)
        
        client.configure_retry(max_retries=10, initial_delay=2.0)
        self.assertEqual(client.max_retries, 10)
        self.assertEqual(client.retry_initial_delay, 2.0)
        
        # 测试只修改部分参数
        client.configure_retry(max_retries=5)
        self.assertEqual(client.max_retries, 5)
        self.assertEqual(client.retry_initial_delay, 2.0)
        
        client.configure_retry(initial_delay=1.5)
        self.assertEqual(client.max_retries, 5)
        self.assertEqual(client.retry_initial_delay, 1.5)

    def test_calculate_retry_delay(self):
        """测试重试延迟计算"""
        client = VectorDBClient(retry_initial_delay=0.5)
        
        # 指数退避算法：delay = initial_delay * (2^retry_count)
        self.assertEqual(client._calculate_retry_delay(0), 0.5)  # 0.5 * (2^0) = 0.5
        self.assertEqual(client._calculate_retry_delay(1), 1.0)  # 0.5 * (2^1) = 1.0
        self.assertEqual(client._calculate_retry_delay(2), 2.0)  # 0.5 * (2^2) = 2.0
        self.assertEqual(client._calculate_retry_delay(3), 4.0)  # 0.5 * (2^3) = 4.0

    def test_headers_without_api_key(self):
        """测试未设置API密钥时获取请求头会抛出异常"""
        client = VectorDBClient()
        with self.assertRaises(VectorDBAuthError) as context:
            client._get_headers()
        
        self.assertIn("API密钥未设置", str(context.exception))

    def test_headers_with_api_key(self):
        """测试设置API密钥后获取请求头"""
        from vikingdb.version import __version__
        
        client = VectorDBClient(api_key="test_api_key")
        headers = client._get_headers()
        
        self.assertEqual(headers["Authorization"], "Bearer test_api_key")
        self.assertEqual(headers["User-Agent"], f"volcstack-python-sdk/{__version__}")
        self.assertEqual(headers["Content-Type"], "application/json")


if __name__ == "__main__":
    unittest.main()