# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Scenario 4 – Search Aggregations
"""
from __future__ import annotations

import json
import os
import time

import pytest

from vikingdb import IAM
from vikingdb.vector import AggRequest, UpsertDataRequest, VikingVector

from .guide_helpers import (
    Clients,
    build_clients,
    build_request_options,
    build_story_chapters,
    chapters_to_upsert,
    cleanup_chapters,
    load_config,
    new_session_tag,
)


def test_snippet_search_aggregate() -> None:
    """
    Inline aggregation example mirroring the Go snippet.
    """
    auth = IAM(
        ak=os.environ["VIKINGDB_AK"],
        sk=os.environ["VIKINGDB_SK"],
    )
    client = VikingVector(
        host=os.environ["VIKINGDB_HOST"],
        region=os.environ["VIKINGDB_REGION"],
        auth=auth,
        scheme="https",
        connection_timeout=30,
        socket_timeout=30,
        user_agent="vikingdb-python-sdk-guide",
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


@pytest.fixture(scope="module")
def aggregate_clients() -> Clients:
    return build_clients(load_config())


def test_scenario_search_extensions_and_analytics(aggregate_clients: Clients) -> None:
    session_tag = new_session_tag("index-extensions")
    request_options = build_request_options(session_tag)
    base_paragraph = int(time.time()) % 1_000_000
    chapters = build_story_chapters(session_tag, base_paragraph)

    try:
        for payload in chapters_to_upsert(chapters):
            aggregate_clients.collection.upsert(
                UpsertDataRequest(data=[payload]),
                request_options=request_options,
            )

        time.sleep(3)

        agg_req = AggRequest(
            field="paragraph",
            op="count",
            cond={"gt": 1},
        )
        response = aggregate_clients.index.aggregate(agg_req, request_options=request_options)
        assert response.result and response.result.agg
        print(f"Aggregate request_id={response.request_id} agg={json.dumps(response.result.agg)}")
    finally:
        cleanup_chapters(aggregate_clients.collection, chapters, request_options=request_options)
