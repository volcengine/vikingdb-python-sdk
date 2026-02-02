# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import time
import json

from vikingdb import IAM
from vikingdb.vector import SearchByKeywordsRequest, UpsertDataRequest, VikingDB


def main() -> None:
    """Inline keyword search over scoped documents."""
    auth = IAM(
        ak=os.environ["VIKINGDB_AK"],
        sk=os.environ["VIKINGDB_SK"],
    )
    client = VikingDB(
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

    base_paragraph = int(time.time() * 1e6) % 1_000_000
    documents = [
        {
            "title": "Signal playbook",
            "paragraph": base_paragraph,
            "score": 86.0,
            "text": "Signal insights tailored for keyword demonstrations.",
        },
        {
            "title": "Session recap",
            "paragraph": base_paragraph + 1,
            "score": 78.0,
            "text": "Recap without keywords to show contrast in results.",
        },
    ]

    for doc in documents:
        collection_client.upsert(UpsertDataRequest(data=[doc]))

    time.sleep(2)

    filter_map = {"op": "range", "field": "paragraph", "gte": base_paragraph, "lt": base_paragraph + len(documents)}
    search_req = SearchByKeywordsRequest(
        keywords=["playbook"],
        limit=2,
        output_fields=["title", "score"],
        filter=filter_map,
    )
    response = index_client.search_by_keywords(search_req)
    hits = response.result.data if response.result and response.result.data else []
    print(f"SearchByKeywords request_id={response.request_id} hits={len(hits)}")
    print(response.model_dump_json(indent=2, by_alias=True) if hasattr(response, "model_dump_json") else json.dumps(response.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()