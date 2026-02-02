# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import json

from vikingdb import IAM
from vikingdb.vector import SearchByRandomRequest, VikingDB


def main() -> None:
    """Connectivity quickstart mirroring the snippet test."""
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
    index_client = client.index(
        collection_name=os.environ["VIKINGDB_COLLECTION"],
        index_name=os.environ["VIKINGDB_INDEX"],
    )

    response = index_client.search_by_random(SearchByRandomRequest(limit=1))
    data = []
    if response.result and response.result.data:
        data = response.result.data
    hits = len(data)
    print(f"SearchByRandom request_id={response.request_id} hits={hits}")
    # Pretty print full JSON response if available
    if hasattr(response, "model_dump"):
        try:
            print(response.model_dump_json(indent=2, by_alias=True) if hasattr(response, "model_dump_json") else json.dumps(response.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))
        except Exception:
            pass


if __name__ == "__main__":
    main()