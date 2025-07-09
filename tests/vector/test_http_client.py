import unittest
from vikingdb.core import base_http_client


class TestHttpClient(unittest.TestCase):
    """测试客户端初始化和配置"""

    def test_default_initialization(self):
        client = base_http_client.BaseHttpClient(scheme="http", host="101.126.39.195", port=None, )
        resp = client.request(method="GET", path="/api/vikingdb/Ping", params={}, headers={})
        print(resp)
        print(resp.status_code)
        print(resp.headers)
        print(resp.text)


