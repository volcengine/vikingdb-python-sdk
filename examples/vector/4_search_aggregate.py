# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
import os
import time

from vikingdb import IAM
from vikingdb.vector import AggRequest, UpsertDataRequest, VikingVector


def main() -> None:
    """Inline aggregation example."""
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
    docs = [
        {"title": "Aggregate intro", "paragraph": base_paragraph, "score": 70.0, "text": "Aggregation example one."},
        {
            "title": "Aggregate follow-up",
            "paragraph": base_paragraph + 1,
            "score": 82.0,
            "text": "Aggregation example two.",
        },
    ]
    for doc in docs:
        collection_client.upsert(UpsertDataRequest(data=[doc]))

    time.sleep(2)

    agg_req = AggRequest(
        field="paragraph",
        op="count",
        cond={"gte": base_paragraph},
    )
    response = index_client.aggregate(agg_req)
    agg = response.result.agg if response.result and response.result.agg else {}
    print(f"Aggregate request_id={response.request_id} agg={json.dumps(agg)}")
    if hasattr(response, "model_dump"):
        try:
            print(response.model_dump_json(indent=2, by_alias=True) if hasattr(response, "model_dump_json") else json.dumps(response.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))
        except Exception:
            pass


if __name__ == "__main__":
    main()