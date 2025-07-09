
from core import base_http_client
from vector import param

class VectorService:
    def __init__(
            self,
            api_key,
            host: str,
            scheme: str = "https",
            port: int = None,
            max_connections: int = 10,
            max_retries: int = 3,
            backoff_factor: float = 0.5,
            timeout: int = 10,
    ):
        self.api_key = api_key
        self.h_client = base_http_client.BaseHttpClient(
            host=host, scheme=scheme, port=port, max_connections=max_connections,
            max_retries=max_retries, backoff_factor=backoff_factor, timeout=timeout,
        )

    # def

    def do_request(self,
            method: str,
            path: str,
            headers: dict = None,
            params: dict = None,
            body_json: dict = None,
            timeout: int = None) -> [int, str]:
        if headers is None:
            headers = {}
        headers.update({
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        })
        resp = self.h_client.request(method=method, path=path, headers=headers, params=params,
                                             body_json=body_json, timeout=timeout)
        return resp.status_code, resp.text

    def fetch_data_in_collection(self, project_name=None, resource_id=None, collection_name=None,
                                 ids=None):
        prm = param.ReqFetchDataInCollection()
        if project_name is not None:
            prm.project_name = project_name
        if resource_id is not None:
            prm.resource_id = resource_id
        if collection_name is not None:
            prm.collection_name = collection_name
        if ids is not None:
            prm.ids = ids

        req_body = prm.model_dump(
            by_alias=True,
            exclude_unset=True,
        )
        status_code, resp_text = self.do_request(
            method="POST",
            path="/api/vikingdb/data/fetch_in_collection",
            body_json=req_body
        )
        print(f"status_code: {status_code}")
        print(f"resp_text: {resp_text}")
        result = param.RespBaseDataApi[param.ResultFetchDataInCollection].model_validate_json(resp_text)
        print(f"result: {result}")
        return result

