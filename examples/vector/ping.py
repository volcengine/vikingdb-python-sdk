# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

import unittest
from vikingdb.core import base_http_client


class TestHttpClient(unittest.TestCase):

    def test_default_initialization(self):
        client = base_http_client.BaseHttpClient(scheme="http", host="api-vikingdb.vikingdb.cn-beijing.volces.com", port=None, )
        resp = client.request(method="GET", path="/api/vikingdb/Ping", params={}, headers={})
        print(resp)
        print(resp.status_code)
        print(resp.headers)
        print(resp.text)


