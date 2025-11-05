# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Scenario 3.1 – Multi-Modal Retrieval With Filters
"""
from __future__ import annotations

import os
import time

import pytest

from vikingdb import IAM
from vikingdb.vector import SearchByMultiModalRequest, UpsertDataRequest, VikingVector

from .guide_helpers import (
    Clients,
    bool_and_filters,
    build_clients,
    build_request_options,
    build_story_chapters,
    chapters_to_upsert,
    cleanup_chapters,
    load_config,
    new_session_tag,
    score_at_least_filter,
    session_paragraph_bounds,
)


def test_snippet_index_search_multimodal() -> None:
    """
    Inline multi-modal search showing filters and output fields.
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

    time.sleep(3)

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


@pytest.fixture(scope="module")
def multimodal_clients() -> Clients:
    return build_clients(load_config())


def test_scenario_index_search_multimodal(multimodal_clients: Clients) -> None:
    session_tag = new_session_tag("index-multimodal")
    request_options = build_request_options(session_tag)
    base_paragraph = int(time.time()) % 1_000_000
    chapters = build_story_chapters(session_tag, base_paragraph)

    try:
        for payload in chapters_to_upsert(chapters):
            multimodal_clients.collection.upsert(
                UpsertDataRequest(data=[payload]),
                request_options=request_options,
            )

        time.sleep(3)

        filters = bool_and_filters(
            [
                session_paragraph_bounds(base_paragraph, len(chapters)),
                score_at_least_filter(85.0),
            ]
        )

        retrieval = next(ch for ch in chapters if ch.key == "retrieval-lab")
        search_req = SearchByMultiModalRequest(
            text=retrieval.text,
            need_instruction=False,
            limit=3,
            output_fields=["title", "score", "paragraph"],
            filter=filters,
        )
        response = multimodal_clients.index.search_by_multi_modal(search_req, request_options=request_options)
        assert response.result and response.result.data
        titles = [hit.fields.get("title") for hit in response.result.data]
        assert retrieval.title in titles
    finally:
        cleanup_chapters(multimodal_clients.collection, chapters, request_options=request_options)
