from vikingdb.vector import service

if __name__ == '__main__':
    svc = service.VectorService(
        api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJWaWtpbmdEQiIsImV4cCI6MTc1MjIyODkzOCwiUG9saWN5VHlwZSI6IlZpa2luZ0RCQVBJV3JpdGUiLCJSZXNvdXJjZUlEIjoidmRiLWZkNDQwNzBjZTI4YTQ5MmM4YmZlZGMwYWRlODZkODE5IiwiQWNjb3VudElEIjoiMjEwMTg1ODQ4NCIsIlVzZXJOYW1lIjoiUkRfVGVzdGluZyIsIlVzZXJJRCI6IjM2OTE0NjI3IiwiQ29sbGVjdGlvbiI6InRlc3RfbGl1eWFuZ19jb2xsX25ld192dHpfMSJ9.TdEC7cOEJi0K5ZnIEf5gpHz75atrDf6npQ-iCawqR5Q",
        host="115.190.90.174",
        scheme="http",
        port=None,
        max_connections=10,
        max_retries=3,
        backoff_factor=0.5,
        timeout=10,
    )
    api_resp = svc.fetch_data_in_collection(collection_name="test_liuyang_coll_new_vtz_1", ids=["1", "2", "3",])
    print("=======")
    print(api_resp.api)
    print(api_resp.request_id)
    print(api_resp.code)
    print(api_resp.result)
    print(api_resp.result.fetch)
    print(api_resp.result.ids_not_exists)
