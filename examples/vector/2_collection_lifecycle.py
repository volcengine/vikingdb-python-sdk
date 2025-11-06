# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import time
import json

from vikingdb import IAM
from vikingdb.vector import (
    DeleteDataRequest,
    FetchDataInCollectionRequest,
    SearchByMultiModalRequest,
    UpdateDataRequest,
    UpsertDataRequest,
    VikingVector,
)


def main() -> None:
    """Inline lifecycle flow: upsert → search → update → fetch → delete."""
    auth = IAM(
        ak=os.environ["VIKINGDB_AK"],
        sk=os.environ["VIKINGDB_SK"],
    )
    client = VikingVector(
        host=os.environ["VIKINGDB_HOST"],
        region=os.environ["VIKINGDB_REGION"],
        auth=auth,
        scheme="https",
        timeout=30,
    )
    collection_client = client.collection(collection_name=os.environ["VIKINGDB_COLLECTION"])
    index_client = client.index(
        collection_name=os.environ["VIKINGDB_COLLECTION"],
        index_name=os.environ["VIKINGDB_INDEX"],
    )

    paragraph = int(time.time() * 1e6) % 1_000_000
    chapter = {
        "title": "Lifecycle quickstart",
        "paragraph": paragraph,
        "score": 42.5,
        "text": "Simple lifecycle payload written inline for the reference flow.",
    }
    upsert_resp = collection_client.upsert(UpsertDataRequest(data=[chapter]))
    print(f"Upsert request_id={upsert_resp.request_id}")
    print(upsert_resp.model_dump_json(indent=2, by_alias=True) if hasattr(upsert_resp, "model_dump_json") else json.dumps(upsert_resp.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))

    time.sleep(2)

    search_req = SearchByMultiModalRequest(
        text="Need the lifecycle quickstart chapter overview",
        need_instruction=False,
        limit=1,
        output_fields=["title", "score"],
    )
    search_resp = index_client.search_by_multi_modal(search_req)
    print(search_resp.model_dump_json(indent=2, by_alias=True) if hasattr(search_resp, "model_dump_json") else json.dumps(search_resp.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))
    if not search_resp.result or not search_resp.result.data:
        print("SearchByMultiModal returned no hits")
        return
    chapter_id = search_resp.result.data[0].id
    if chapter_id is None:
        print("SearchByMultiModal response missing chapter id")
        return

    new_score = 47.0
    update_resp = collection_client.update(
        UpdateDataRequest(data=[{"__AUTO_ID__": chapter_id, "score": new_score}])
    )
    print(f"Update request_id={update_resp.request_id}")
    print(update_resp.model_dump_json(indent=2, by_alias=True) if hasattr(update_resp, "model_dump_json") else json.dumps(update_resp.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))

    fetch_resp = collection_client.fetch(FetchDataInCollectionRequest(ids=[chapter_id]))
    print(fetch_resp.model_dump_json(indent=2, by_alias=True) if hasattr(fetch_resp, "model_dump_json") else json.dumps(fetch_resp.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))
    if fetch_resp.result and fetch_resp.result.items:
        fetched = fetch_resp.result.items[0].fields.get("score")
        fetched_score = float(fetched) if fetched is not None else None
        print(f"Fetch request_id={fetch_resp.request_id} score={fetched_score}")

    delete_resp = collection_client.delete(DeleteDataRequest(ids=[chapter_id]))
    print(f"Delete request_id={delete_resp.request_id}")
    print(delete_resp.model_dump_json(indent=2, by_alias=True) if hasattr(delete_resp, "model_dump_json") else json.dumps(delete_resp.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()