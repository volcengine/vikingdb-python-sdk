# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

import datetime
import hashlib
import hmac
from urllib.parse import quote

import requests, json

def norm_query(params):
    query = ""
    for key in sorted(params.keys()):
        if type(params[key]) == list:
            for k in params[key]:
                query = (
                    query + quote(key, safe="-_.~") + "=" + quote(k, safe="-_.~") + "&"
                )
        else:
            query = (query + quote(key, safe="-_.~") + "=" + quote(params[key], safe="-_.~") + "&")
    query = query[:-1]
    return query.replace("+", "%20")

def hmac_sha256(key: bytes, content: str):
    return hmac.new(key, content.encode("utf-8"), hashlib.sha256).digest()

def hash_sha256(content: str):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

class ClientForAkSk:
    def __init__(self, ak, sk, host, region, scheme="https", service_code="vikingdb"):
        self.ak = ak
        self.sk = sk
        self.host = host
        self.region = region
        self.scheme = scheme
        self.service_code = service_code

    def request(self, method, body, path, query=None, header=None):
        if query is None:
            query = {}
        if header is None:
            header = {}
        credential = {
            "access_key_id": self.ak,
            "secret_access_key": self.sk,
            "service": self.service_code,
            "region": self.region,
        }
        request_param = {
            "body": json.dumps(body),
            "host": self.host,
            "path": path,
            "method": method,
            "content_type": 'application/json',
            "date": datetime.datetime.utcnow(),
            "query": {**query},
        }
        if body is None:
            request_param["body"] = ""
        x_date = request_param["date"].strftime("%Y%m%dT%H%M%SZ")
        short_x_date = x_date[:8]
        x_content_sha256 = hash_sha256(request_param["body"])
        sign_result = {
            "Host": request_param["host"],
            "X-Content-Sha256": x_content_sha256,
            "X-Date": x_date,
            "Content-Type": request_param["content_type"],
        }
        signed_headers_str = ";".join(
            ["content-type", "host", "x-content-sha256", "x-date"]
        )
        canonical_request_str = "\n".join(
            [request_param["method"].upper(),
             request_param["path"],
             norm_query(request_param["query"]),
             "\n".join(
                 [
                     "content-type:" + request_param["content_type"],
                     "host:" + request_param["host"],
                     "x-content-sha256:" + x_content_sha256,
                     "x-date:" + x_date,
                 ]
             ),
             "",
             signed_headers_str,
             x_content_sha256,
             ]
        )

        hashed_canonical_request = hash_sha256(canonical_request_str)
        credential_scope = "/".join([short_x_date, credential["region"], credential["service"], "request"])
        string_to_sign = "\n".join(["HMAC-SHA256", x_date, credential_scope, hashed_canonical_request])

        k_date = hmac_sha256(credential["secret_access_key"].encode("utf-8"), short_x_date)
        k_region = hmac_sha256(k_date, credential["region"])
        k_service = hmac_sha256(k_region, credential["service"])
        k_signing = hmac_sha256(k_service, "request")
        signature = hmac_sha256(k_signing, string_to_sign).hex()

        sign_result["Authorization"] = "HMAC-SHA256 Credential={}, SignedHeaders={}, Signature={}".format(
            credential["access_key_id"] + "/" + credential_scope,
            signed_headers_str,
            signature,
        )
        header = {**header, **sign_result}
        r = requests.request(method=method,
                             url="{}://{}{}".format(self.scheme, request_param["host"], request_param["path"]),
                             headers=header,
                             params=request_param["query"],
                             data=request_param["body"],
                             )
        return r.status_code, r.headers, r.json()
