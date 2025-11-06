# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import time
import json

from vikingdb import IAM
from vikingdb.vector import SearchByMultiModalRequest, UpsertDataRequest, VikingVector


def main() -> None:
    """Inline multi-modal search showing filters and output fields."""
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

    base_paragraph = int(time.time() * 1e6) % 1_000_000
    chapters = [
        {
            "title": "Session kickoff",
            "paragraph": base_paragraph,
            "score": 73.0,
            "text": "This kickoff chapter keeps the reference search grounded.",
        },
        {
            "title": "Session filters",
            "paragraph": base_paragraph + 1,
            "score": 91.0,
            "text": "Filter walkthrough for multi-modal search.",
        },
    ]

    for payload in chapters:
        collection_client.upsert(UpsertDataRequest(data=[payload]))

    time.sleep(2)

    filter_map = {"op": "range", "field": "paragraph", "gte": base_paragraph, "lte": base_paragraph + 1}
    search_req = SearchByMultiModalRequest(
        text="Which chapter explains the session filters?",
        need_instruction=False,
        limit=2,
        output_fields=["title", "score", "paragraph"],
        filter=filter_map,
    )
    response = index_client.search_by_multi_modal(search_req)
    hits = response.result.data if response.result and response.result.data else []
    print(f"SearchByMultiModal request_id={response.request_id} hits={len(hits)}")
    print(response.model_dump_json(indent=2, by_alias=True) if hasattr(response, "model_dump_json") else json.dumps(response.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()