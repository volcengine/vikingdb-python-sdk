# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Scenario 3.3 – Keyword Retrieval
"""
from __future__ import annotations

import os
import time

import pytest

from vikingdb import IAM
from vikingdb.vector import SearchByKeywordsRequest, UpsertDataRequest, VikingVector

from .guide_helpers import (
    Clients,
    assert_keyword_hit_titles,
    build_clients,
    build_request_options,
    build_story_chapters,
    chapters_to_upsert,
    cleanup_chapters,
    load_config,
    new_session_tag,
    session_paragraph_bounds,
)


def test_snippet_search_keywords() -> None:
    """
    Inline keyword search over scoped documents, mirroring the Go snippet.
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

    time.sleep(3)

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


@pytest.fixture(scope="module")
def keyword_clients() -> Clients:
    return build_clients(load_config())


def test_scenario_search_keywords(keyword_clients: Clients) -> None:
    session_tag = new_session_tag("index-extensions")
    request_options = build_request_options(session_tag)
    base_paragraph = int(time.time()) % 1_000_000
    chapters = build_story_chapters(session_tag, base_paragraph)

    try:
        for payload in chapters_to_upsert(chapters):
            keyword_clients.collection.upsert(
                UpsertDataRequest(data=[payload]),
                request_options=request_options,
            )

        time.sleep(5)

        filter_map = session_paragraph_bounds(base_paragraph, len(chapters))
        search_req = SearchByKeywordsRequest(
            keywords=["Signal"],
            limit=3,
            output_fields=["title", "score", "text"],
            filter=filter_map,
        )
        response = keyword_clients.index.search_by_keywords(search_req, request_options=request_options)
        titles, request_id = assert_keyword_hit_titles(
            response,
            expected_keyword="Signal",
            session_tag=session_tag,
        )
        print(f"SearchByKeywords request_id={request_id} hits={len(titles)}")
    finally:
        cleanup_chapters(keyword_clients.collection, chapters, request_options=request_options)
