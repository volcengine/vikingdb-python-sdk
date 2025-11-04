# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Scenario 2 – Collection Lifecycle

Follows the Go reference by showing both an inline lifecycle walkthrough and a helper-based scenario.
"""
from __future__ import annotations

import os
import time

import pytest

from vikingdb import IAM
from vikingdb.vector import (
    DeleteDataRequest,
    FetchDataInCollectionRequest,
    SearchByMultiModalRequest,
    UpdateDataRequest,
    UpsertDataRequest,
    VikingVector,
)

from .guide_helpers import (
    Clients,
    assign_chapter_ids_via_search,
    build_clients,
    build_request_options,
    build_story_chapters,
    chapters_to_upsert,
    cleanup_chapters,
    load_config,
    new_session_tag,
)


def test_snippet_collection_lifecycle() -> None:
    """
    Inline lifecycle flow mirroring the Go snippet:
      1. Upsert a chapter.
      2. Search to hydrate the chapter ID.
      3. Update scalar fields.
      4. Fetch to verify.
      5. Delete the record.
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

    paragraph = int(time.time() * 1e6) % 1_000_000
    chapter = {
        "title": "Lifecycle quickstart",
        "paragraph": paragraph,
        "score": 42.5,
        "text": "Simple lifecycle payload written inline for the reference flow.",
    }
    upsert_resp = collection_client.upsert(UpsertDataRequest(data=[chapter]))
    print(f"Upsert request_id={upsert_resp.request_id}")

    time.sleep(2)

    search_req = SearchByMultiModalRequest(
        text="Need the lifecycle quickstart chapter overview",
        need_instruction=False,
        limit=1,
        output_fields=["title", "score"],
    )
    search_resp = index_client.search_by_multi_modal(search_req)
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

    fetch_resp = collection_client.fetch(FetchDataInCollectionRequest(ids=[chapter_id]))
    if fetch_resp.result and fetch_resp.result.items:
        fetched = fetch_resp.result.items[0].fields.get("score")
        fetched_score = float(fetched) if fetched is not None else None
        print(f"Fetch request_id={fetch_resp.request_id} score={fetched_score}")

    delete_resp = collection_client.delete(DeleteDataRequest(ids=[chapter_id]))
    print(f"Delete request_id={delete_resp.request_id}")


@pytest.fixture(scope="module")
def collection_clients() -> Clients:
    return build_clients(load_config())


def test_scenario_collection_lifecycle(collection_clients: Clients) -> None:
    session_tag = new_session_tag("collection-lifecycle")
    request_options = build_request_options(session_tag)
    base_paragraph = int(time.time()) % 1_000_000
    chapters = build_story_chapters(session_tag, base_paragraph)

    try:
        for payload in chapters_to_upsert(chapters):
            response = collection_clients.collection.upsert(
                UpsertDataRequest(data=[payload]),
                request_options=request_options,
            )
            assert response.request_id

        assign_chapter_ids_via_search(
            collection_clients.index,
            chapters,
            output_fields=["title", "paragraph", "score"],
            request_options=request_options,
        )

        target = next(ch for ch in chapters if ch.key == "retrieval-lab")
        assert target.chapter_id is not None

        new_score = target.score + 4.25
        update_resp = collection_clients.collection.update(
            UpdateDataRequest(data=[{"__AUTO_ID__": target.chapter_id, "score": new_score}]),
            request_options=request_options,
        )
        assert update_resp.request_id

        fetch_resp = collection_clients.collection.fetch(
            FetchDataInCollectionRequest(ids=[target.chapter_id]),
            request_options=request_options,
        )
        assert fetch_resp.result and fetch_resp.result.items
        fetched_score = fetch_resp.result.items[0].fields.get("score")
        assert fetched_score == pytest.approx(new_score)
    finally:
        cleanup_chapters(collection_clients.collection, chapters, request_options=request_options)
