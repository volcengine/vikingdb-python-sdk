"""
测试请求构建和头部设置
"""

import json
import unittest
from unittest import mock
from urllib.request import Request

from vikingdb.core.client import VectorDBClient
from vikingdb.version import __version__


class TestRequestBuilding(unittest.TestCase):
    """测试请求构建和头部设置"""

    def setUp(self):
        """测试前准备"""
        self.client = VectorDBClient(api_key="test_api_key")
        
        # 创建urlopen的模拟对象
        self.urlopen_patcher = mock.patch('urllib.request.urlopen')
        self.mock_urlopen = self.urlopen_patcher.start()
        
        # 设置模拟响应
        self.mock_response = mock.Mock()
        self.mock_response.read.return_value = json.dumps({
            "api": "test",
            "request_id": "req123",
            "code": "Success",
            "message": "操作成功",
            "result": {"data": "test_data"}
        }).encode('utf-8')
        self.mock_urlopen.return_value.__enter__.return_value = self.mock_response
    
    def tearDown(self):
        """测试后清理"""
        self.urlopen_patcher.stop()
    
    def test_get_request(self):
        """测试GET请求构建"""
        with mock.patch('urllib.request.Request') as mock_request:
            self.client.get("/test", params={"param1": "value1"})
            
            # 验证Request的调用参数
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            
            self.assertEqual(kwargs['url'], "https://api.volcstack.com/test?param1=value1")
            self.assertEqual(kwargs['method'], "GET")
            self.assertIsNone(kwargs['data'])
            self.assertEqual(kwargs['headers']['Authorization'], "Bearer test_api_key")
            self.assertEqual(kwargs['headers']['User-Agent'], f"volcstack-python-sdk/{__version__}")
            self.assertEqual(kwargs['headers']['Content-Type'], "application/json")
    
    def test_post_request_with_data(self):
        """测试带数据的POST请求构建"""
        test_data = {"key": "value"}
        
        with mock.patch('urllib.request.Request') as mock_request:
            self.client.post("/test", data=test_data)
            
            # 验证Request的调用参数
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            
            self.assertEqual(kwargs['url'], "https://api.volcstack.com/test")
            self.assertEqual(kwargs['method'], "POST")
            self.assertEqual(json.loads(kwargs['data'].decode('utf-8')), test_data)
            self.assertEqual(kwargs['headers']['Authorization'], "Bearer test_api_key")
    
    def test_put_request(self):
        """测试PUT请求构建"""
        test_data = {"key": "value"}
        
        with mock.patch('urllib.request.Request') as mock_request:
            self.client.put("/test", data=test_data, params={"param1": "value1"})
            
            # 验证Request的调用参数
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            
            self.assertEqual(kwargs['url'], "https://api.volcstack.com/test?param1=value1")
            self.assertEqual(kwargs['method'], "PUT")
            self.assertEqual(json.loads(kwargs['data'].decode('utf-8')), test_data)
    
    def test_delete_request(self):
        """测试DELETE请求构建"""
        with mock.patch('urllib.request.Request') as mock_request:
            self.client.delete("/test", params={"id": "123"})
            
            # 验证Request的调用参数
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            
            self.assertEqual(kwargs['url'], "https://api.volcstack.com/test?id=123")
            self.assertEqual(kwargs['method'], "DELETE")
            self.assertIsNone(kwargs['data'])
    
    def test_create_vector_method(self):
        """测试创建向量方法的请求构建"""
        vector_data = {
            "id": "vec1",
            "values": [0.1, 0.2, 0.3],
            "metadata": {"text": "测试向量"}
        }
        
        with mock.patch('urllib.request.Request') as mock_request:
            self.client.create_vector(vector_data)
            
            # 验证Request的调用参数
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            
            self.assertEqual(kwargs['url'], "https://api.volcstack.com/vectors")
            self.assertEqual(kwargs['method'], "POST")
            self.assertEqual(json.loads(kwargs['data'].decode('utf-8')), vector_data)


if __name__ == "__main__":
    unittest.main()