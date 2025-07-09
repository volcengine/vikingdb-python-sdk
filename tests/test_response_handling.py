"""
测试响应处理和错误处理
"""

import json
import unittest
from unittest import mock
from urllib.error import HTTPError, URLError

from vikingdb.core.client import VectorDBClient
from vikingdb.core.exceptions import (
    VectorDBError,
    VectorDBRequestError,
    VectorDBResponseError
)


class TestResponseHandling(unittest.TestCase):
    """测试响应处理和错误处理"""

    def setUp(self):
        """测试前准备"""
        self.client = VectorDBClient(api_key="test_api_key")
        
        # 创建urlopen的模拟对象
        self.urlopen_patcher = mock.patch('urllib.request.urlopen')
        self.mock_urlopen = self.urlopen_patcher.start()
    
    def tearDown(self):
        """测试后清理"""
        self.urlopen_patcher.stop()
    
    def test_successful_response(self):
        """测试成功响应的处理"""
        # 设置模拟响应
        mock_response = mock.Mock()
        mock_response.read.return_value = json.dumps({
            "api": "test",
            "request_id": "req123",
            "code": "Success",
            "message": "操作成功",
            "result": {"data": "test_data"}
        }).encode('utf-8')
        self.mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # 发送请求
        result = self.client.get("/test")
        
        # 验证结果
        self.assertEqual(result["api"], "test")
        self.assertEqual(result["request_id"], "req123")
        self.assertEqual(result["code"], "Success")
        self.assertEqual(result["result"]["data"], "test_data")
    
    def test_api_error_response(self):
        """测试API错误响应的处理"""
        # 设置模拟响应
        mock_response = mock.Mock()
        mock_response.read.return_value = json.dumps({
            "api": "test",
            "request_id": "req123",
            "code": "InvalidParameter",
            "message": "参数无效"
        }).encode('utf-8')
        self.mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # 发送请求并验证异常
        with self.assertRaises(VectorDBError) as context:
            self.client.get("/test")
        
        # 验证异常信息
        exception = context.exception
        self.assertEqual(exception.code, "InvalidParameter")
        self.assertEqual(exception.message, "参数无效")
        self.assertEqual(exception.request_id, "req123")
    
    def test_http_error(self):
        """测试HTTP错误的处理"""
        # 创建HTTP错误
        mock_error = HTTPError(
            url="https://api.volcstack.com/test",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=mock.Mock()
        )
        mock_error.read = mock.Mock(return_value=json.dumps({
            "request_id": "req123",
            "code": "ResourceNotFound",
            "message": "资源不存在"
        }).encode('utf-8'))
        
        # 设置urlopen抛出HTTP错误
        self.mock_urlopen.side_effect = mock_error
        
        # 发送请求并验证异常
        with self.assertRaises(VectorDBError) as context:
            self.client.get("/test")
        
        # 验证异常信息
        exception = context.exception
        self.assertEqual(exception.code, "ResourceNotFound")
        self.assertEqual(exception.message, "资源不存在")
        self.assertEqual(exception.request_id, "req123")
        self.assertEqual(exception.status_code, 404)
    
    def test_http_error_invalid_json(self):
        """测试HTTP错误返回无效JSON的处理"""
        # 创建HTTP错误
        mock_error = HTTPError(
            url="https://api.volcstack.com/test",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=mock.Mock()
        )
        mock_error.read = mock.Mock(return_value=b"Not a JSON response")
        
        # 设置urlopen抛出HTTP错误
        self.mock_urlopen.side_effect = mock_error
        
        # 发送请求并验证异常
        with self.assertRaises(VectorDBRequestError) as context:
            self.client.get("/test")
        
        # 验证异常信息
        self.assertIn("HTTP错误: 500", str(context.exception))
    
    def test_url_error(self):
        """测试URL错误的处理"""
        # 创建URL错误
        mock_error = URLError(reason="连接超时")
        
        # 设置urlopen抛出URL错误
        self.mock_urlopen.side_effect = mock_error
        
        # 发送请求并验证异常
        with self.assertRaises(VectorDBRequestError) as context:
            self.client.get("/test")
        
        # 验证异常信息
        self.assertIn("网络错误: 连接超时", str(context.exception))
    
    def test_invalid_json_response(self):
        """测试无效JSON响应的处理"""
        # 设置模拟响应
        mock_response = mock.Mock()
        mock_response.read.return_value = b"Not a JSON response"
        self.mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # 发送请求并验证异常
        with self.assertRaises(VectorDBResponseError) as context:
            self.client.get("/test")
        
        # 验证异常信息
        self.assertIn("无法解析API响应", str(context.exception))


class TestRetryMechanism(unittest.TestCase):
    """测试重试机制"""

    def setUp(self):
        """测试前准备"""
        # 创建urlopen的模拟对象
        self.urlopen_patcher = mock.patch('urllib.request.urlopen')
        self.mock_urlopen = self.urlopen_patcher.start()
        
        # 创建time.sleep的模拟对象，避免实际等待
        self.sleep_patcher = mock.patch('time.sleep')
        self.mock_sleep = self.sleep_patcher.start()
    
    def tearDown(self):
        """测试后清理"""
        self.urlopen_patcher.stop()
        self.sleep_patcher.stop()
    
    def test_retry_disabled_on_429(self):
        """测试禁用重试时遇到429错误的处理"""
        # 创建客户端，禁用重试
        client = VectorDBClient(api_key="test_api_key", retry_enabled=False)
        
        # 创建HTTP错误
        mock_error = HTTPError(
            url="https://api.volcstack.com/test",
            code=429,
            msg="Too Many Requests",
            hdrs={},
            fp=mock.Mock()
        )
        mock_error.read = mock.Mock(return_value=json.dumps({
            "request_id": "req123",
            "code": "TooManyRequests",
            "message": "请求过于频繁，请稍后再试"
        }).encode('utf-8'))
        
        # 设置urlopen抛出HTTP错误
        self.mock_urlopen.side_effect = mock_error
        
        # 发送请求并验证异常
        with self.assertRaises(VectorDBError) as context:
            client.get("/test")
        
        # 验证异常信息
        exception = context.exception
        self.assertEqual(exception.code, "TooManyRequests")
        self.assertEqual(exception.status_code, 429)
        
        # 验证没有调用sleep（没有重试）
        self.mock_sleep.assert_not_called()
    
    def test_retry_enabled_on_429(self):
        """测试启用重试时遇到429错误的处理"""
        # 创建客户端，启用重试
        client = VectorDBClient(
            api_key="test_api_key", 
            retry_enabled=True,
            max_retries=2,
            retry_initial_delay=0.5
        )
        
        # 创建HTTP错误
        mock_error = HTTPError(
            url="https://api.volcstack.com/test",
            code=429,
            msg="Too Many Requests",
            hdrs={},
            fp=mock.Mock()
        )
        mock_error.read = mock.Mock(return_value=json.dumps({
            "request_id": "req123",
            "code": "TooManyRequests",
            "message": "请求过于频繁，请稍后再试"
        }).encode('utf-8'))
        
        # 设置成功响应
        mock_success = mock.Mock()
        mock_success.read.return_value = json.dumps({
            "api": "test",
            "request_id": "req124",
            "code": "Success",
            "message": "操作成功",
            "result": {"data": "test_data"}
        }).encode('utf-8')
        
        # 设置urlopen先抛出两次HTTP错误，然后返回成功响应
        self.mock_urlopen.side_effect = [mock_error, mock_error, mock_success]
        
        # 发送请求
        result = client.get("/test")
        
        # 验证结果
        self.assertEqual(result["code"], "Success")
        self.assertEqual(result["result"]["data"], "test_data")
        
        # 验证sleep被调用了两次，且延迟时间符合指数退避算法
        self.assertEqual(self.mock_sleep.call_count, 2)
        self.mock_sleep.assert_any_call(0.5)  # 第一次重试：0.5 * (2^0)
        self.mock_sleep.assert_any_call(1.0)  # 第二次重试：0.5 * (2^1)
    
    def test_retry_max_attempts_exceeded(self):
        """测试超过最大重试次数的处理"""
        # 创建客户端，启用重试
        client = VectorDBClient(
            api_key="test_api_key", 
            retry_enabled=True,
            max_retries=2,
            retry_initial_delay=0.5
        )
        
        # 创建HTTP错误
        mock_error = HTTPError(
            url="https://api.volcstack.com/test",
            code=429,
            msg="Too Many Requests",
            hdrs={},
            fp=mock.Mock()
        )
        mock_error.read = mock.Mock(return_value=json.dumps({
            "request_id": "req123",
            "code": "TooManyRequests",
            "message": "请求过于频繁，请稍后再试"
        }).encode('utf-8'))
        
        # 设置urlopen始终抛出HTTP错误
        self.mock_urlopen.side_effect = mock_error
        
        # 发送请求并验证异常
        with self.assertRaises(VectorDBError) as context:
            client.get("/test")
        
        # 验证异常信息
        exception = context.exception
        self.assertEqual(exception.code, "TooManyRequests")
        self.assertEqual(exception.status_code, 429)
        
        # 验证sleep被调用了最大重试次数
        self.assertEqual(self.mock_sleep.call_count, 2)
        self.mock_sleep.assert_any_call(0.5)  # 第一次重试：0.5 * (2^0)
        self.mock_sleep.assert_any_call(1.0)  # 第二次重试：0.5 * (2^1)
    
    def test_retry_only_on_429(self):
        """测试只在429错误时重试"""
        # 创建客户端，启用重试
        client = VectorDBClient(
            api_key="test_api_key", 
            retry_enabled=True,
            max_retries=2
        )
        
        # 创建HTTP错误（非429）
        mock_error = HTTPError(
            url="https://api.volcstack.com/test",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=mock.Mock()
        )
        mock_error.read = mock.Mock(return_value=json.dumps({
            "request_id": "req123",
            "code": "InternalError",
            "message": "服务器内部错误"
        }).encode('utf-8'))
        
        # 设置urlopen抛出HTTP错误
        self.mock_urlopen.side_effect = mock_error
        
        # 发送请求并验证异常
        with self.assertRaises(VectorDBError) as context:
            client.get("/test")
        
        # 验证异常信息
        exception = context.exception
        self.assertEqual(exception.code, "InternalError")
        self.assertEqual(exception.status_code, 500)
        
        # 验证没有调用sleep（没有重试）
        self.mock_sleep.assert_not_called()


if __name__ == "__main__":
    unittest.main()