# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Consolidated Scenario Tests for VikingDB Python Guides

This module extracts all `test_scenario_*` tests from the E* guide modules into a single file.
Run with:
    pytest -q examples/vector/viking_test.py
"""
from __future__ import annotations

import json
import os
import time

import pytest
from vikingdb import IAM
from vikingdb.vector import (
    AggRequest,
    EmbeddingModelOpt,
    EmbeddingRequest,
    SearchByKeywordsRequest,
    SearchByMultiModalRequest,
    SearchByRandomRequest,
    SearchByVectorRequest,
    UpsertDataRequest,
    VikingVector,
)

from .test_helper import (
    Clients,
    EnvConfig,
    DEFAULT_REGION,
    EMBEDDING_MODEL_NAME,
    TEXT_COLLECTION,
    TEXT_INDEX,
    VECTOR_COLLECTION,
    VECTOR_INDEX,
    require_env_vars,
    load_config,
    build_clients,
    embed_dense_vectors,
    StoryChapter,
    build_story_chapters,
    chapters_to_upsert,
    assign_chapter_ids_via_search,
    search_chapter_by_narrative,
)


# Replace multiple clients fixtures with a single shared VikingVector client
@pytest.fixture(scope="module")
def viking() -> VikingVector:
    cfg = load_config()
    auth = IAM(ak=cfg.access_key, sk=cfg.secret_key)
    return VikingVector(host=cfg.host, region=cfg.region, scheme=cfg.scheme, auth=auth, timeout=30)


# Scenario 1 – Connectivity

def test_scenario_connectivity(viking: VikingVector) -> None:
    session_tag = new_session_tag("scenario-connectivity")
    request_options = build_request_options(session_tag)
    cfg = load_config()
    index_client = viking.index(
        collection_name=cfg.collection,
        index_name=cfg.index,
        project_name=cfg.project_name,
        resource_id=cfg.resource_id,
    )
    collection_client = viking.collection(
        collection_name=cfg.collection,
        project_name=cfg.project_name,
        resource_id=cfg.resource_id,
    )
    embedding_client = viking.embedding()
    response = index_client.search_by_random(SearchByRandomRequest(limit=1), request_options=request_options)
    assert response.request_id
    assert collection_client is not None
    assert embedding_client is not None
    hits = 0 if not response.result or not response.result.data else len(response.result.data)
    print(
        f"Connectivity check host={os.getenv('VIKINGDB_HOST', 'default-host')} "
        f"region={os.getenv('VIKINGDB_REGION', 'default-region')} "
        f"request_id={response.request_id} hits={hits}"
    )


# Scenario 2 – Collection Lifecycle

def test_scenario_collection_lifecycle(viking: VikingVector) -> None:
    session_tag = new_session_tag("collection-lifecycle")
    request_options = build_request_options(session_tag)
    base_paragraph = int(time.time()) % 1_000_000
    chapters = build_story_chapters(session_tag, base_paragraph)
    cfg = load_config()
    collection_client = viking.collection(
        collection_name=cfg.collection,
        project_name=cfg.project_name,
        resource_id=cfg.resource_id,
    )
    index_client = viking.index(
        collection_name=cfg.collection,
        index_name=cfg.index,
        project_name=cfg.project_name,
        resource_id=cfg.resource_id,
    )

    try:
        for payload in chapters_to_upsert(chapters):
            response = collection_client.upsert(
                UpsertDataRequest(data=[payload]),
                request_options=request_options,
            )
            assert response.request_id

        assign_chapter_ids_via_search(
            index_client,
            chapters,
            output_fields=["title", "paragraph", "score"],
            request_options=request_options,
        )

        target = next(ch for ch in chapters if ch.key == "retrieval-lab")
        assert target.chapter_id is not None

        new_score = target.score + 4.25
        update_resp = collection_client.update(
            {"data": [{"__AUTO_ID__": target.chapter_id, "score": new_score}]},
            request_options=request_options,
        )
        assert update_resp.request_id

        fetch_resp = collection_client.fetch(
            {"ids": [target.chapter_id]},
            request_options=request_options,
        )
        assert fetch_resp.result and fetch_resp.result.items
        fetched_score = fetch_resp.result.items[0].fields.get("score")
        assert fetched_score == pytest.approx(new_score)
    finally:
        cleanup_chapters(collection_client, chapters, request_options=request_options)


# Scenario 3.1 – Multi-Modal Retrieval With Filters

def test_scenario_index_search_multimodal(viking: VikingVector) -> None:
    session_tag = new_session_tag("index-multimodal")
    request_options = build_request_options(session_tag)
    base_paragraph = int(time.time()) % 1_000_000
    chapters = build_story_chapters(session_tag, base_paragraph)
    cfg = load_config()
    collection_client = viking.collection(
        collection_name=cfg.collection,
        project_name=cfg.project_name,
        resource_id=cfg.resource_id,
    )
    index_client = viking.index(
        collection_name=cfg.collection,
        index_name=cfg.index,
        project_name=cfg.project_name,
        resource_id=cfg.resource_id,
    )

    try:
        for payload in chapters_to_upsert(chapters):
            collection_client.upsert(
                UpsertDataRequest(data=[payload]),
                request_options=request_options,
            )

        time.sleep(2)

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
        response = index_client.search_by_multi_modal(search_req, request_options=request_options)
        assert response.result and response.result.data
        titles = [hit.fields.get("title") for hit in response.result.data]
        assert retrieval.title in titles
    finally:
        cleanup_chapters(collection_client, chapters, request_options=request_options)


# Scenario 3.2 – Vector Retrieval With Embeddings

def test_scenario_index_search_vector(viking: VikingVector) -> None:
    session_tag = new_session_tag("search-vector")
    request_options = build_request_options(session_tag)
    base_paragraph = int(time.time()) % 1_000_000
    chapters = build_story_chapters(session_tag, base_paragraph)
    cfg = load_config(collection=VECTOR_COLLECTION, index=VECTOR_INDEX)
    collection_client = viking.collection(
        collection_name=cfg.collection,
        project_name=cfg.project_name,
        resource_id=cfg.resource_id,
    )
    index_client = viking.index(
        collection_name=cfg.collection,
        index_name=cfg.index,
        project_name=cfg.project_name,
        resource_id=cfg.resource_id,
    )
    embedding_client = viking.embedding()

    try:
        chapter_vectors = embed_dense_vectors(
            embedding_client,
            [chapter.text for chapter in chapters],
            request_options=request_options,
        )

        payload = []
        for chapter, vector in zip(chapters, chapter_vectors):
            payload.append(
                {
                    "title": chapter.title,
                    "paragraph": chapter.paragraph,
                    "score": chapter.score,
                    "text": chapter.text,
                    "vector": vector,
                }
            )
        collection_client.upsert(UpsertDataRequest(data=payload), request_options=request_options)

        time.sleep(2)

        retrieval = next(ch for ch in chapters if ch.key == "retrieval-lab")
        query_vector = embed_dense_vectors(
            embedding_client,
            [retrieval.text],
            request_options=request_options,
        )[0]

        filter_map = session_paragraph_bounds(base_paragraph, len(chapters))
        search_req = SearchByVectorRequest(
            dense_vector=query_vector,
            limit=5,
            output_fields=["title", "score", "paragraph"],
            filter=filter_map,
        )
        response = index_client.search_by_vector(search_req, request_options=request_options)
        assert response.result and response.result.data
        titles = [hit.fields.get("title") for hit in response.result.data]
        assert retrieval.title in titles
    finally:
        cleanup_chapters(collection_client, chapters, request_options=request_options)


# Scenario 3.3 – Keyword Retrieval

def test_scenario_search_keywords(viking: VikingVector) -> None:
    session_tag = new_session_tag("index-extensions")
    request_options = build_request_options(session_tag)
    request_options.max_attempts = 5
    base_paragraph = int(time.time()) % 1_000_000
    chapters = build_story_chapters(session_tag, base_paragraph)
    cfg = load_config()
    collection_client = viking.collection(
        collection_name=cfg.collection,
        project_name=cfg.project_name,
        resource_id=cfg.resource_id,
    )
    index_client = viking.index(
        collection_name=cfg.collection,
        index_name=cfg.index,
        project_name=cfg.project_name,
        resource_id=cfg.resource_id,
    )

    try:
        for payload in chapters_to_upsert(chapters):
            collection_client.upsert(
                UpsertDataRequest(data=[payload]),
                request_options=request_options,
            )

        time.sleep(2)

        filter_map = session_paragraph_bounds(base_paragraph, len(chapters))
        search_req = SearchByKeywordsRequest(
            keywords=["Signal"],
            limit=3,
            output_fields=["title", "score", "text"],
            filter=filter_map,
        )
        response = index_client.search_by_keywords(search_req, request_options=request_options)
        titles, request_id = assert_keyword_hit_titles(
            response,
            expected_keyword="Signal",
            session_tag=session_tag,
        )
        print(f"SearchByKeywords request_id={request_id} hits={len(titles)}")
    finally:
        cleanup_chapters(collection_client, chapters, request_options=request_options)


# Scenario 4 – Search Aggregations

def test_scenario_search_extensions_and_analytics(viking: VikingVector) -> None:
    session_tag = new_session_tag("index-extensions")
    request_options = build_request_options(session_tag)
    base_paragraph = int(time.time()) % 1_000_000
    chapters = build_story_chapters(session_tag, base_paragraph)
    cfg = load_config()
    collection_client = viking.collection(
        collection_name=cfg.collection,
        project_name=cfg.project_name,
        resource_id=cfg.resource_id,
    )
    index_client = viking.index(
        collection_name=cfg.collection,
        index_name=cfg.index,
        project_name=cfg.project_name,
        resource_id=cfg.resource_id,
    )

    try:
        for payload in chapters_to_upsert(chapters):
            collection_client.upsert(
                UpsertDataRequest(data=[payload]),
                request_options=request_options,
            )

        time.sleep(2)

        agg_req = AggRequest(
            field="paragraph",
            op="count",
            cond={"gt": 1},
        )
        response = index_client.aggregate(agg_req, request_options=request_options)
        assert response.result and response.result.agg
        print(f"Aggregate request_id={response.request_id} agg={json.dumps(response.result.agg)}")
    finally:
        cleanup_chapters(collection_client, chapters, request_options=request_options)


# Scenario 5 – Embedding Pipelines

def test_scenario_embedding_multimodal_pipeline(viking: VikingVector) -> None:
    session_tag = new_session_tag("embedding-multimodal")
    request_options = build_request_options(session_tag)

    embedding_client = viking.embedding()
    text = "generate embeddings with VikingDB"
    request = EmbeddingRequest(
        dense_model=EmbeddingModelOpt(name="doubao-embedding-vision", version="250615"),
        sparse_model=EmbeddingModelOpt(name="bge-m3"),
        data=[
            {"full_modal_seq": [{"text": text}]},
        ],
    )
    response = embedding_client.embedding(request, request_options=request_options)
    assert response.result and response.result.data
    item = response.result.data[0]
    assert item.dense and len(item.dense) > 0



def test_scenario_embedding_ds_pipeline(viking: VikingVector) -> None:
    session_tag = new_session_tag("embedding-ds")
    request_options = build_request_options(session_tag)

    embedding_client = viking.embedding()
    request = EmbeddingRequest(
        dense_model=EmbeddingModelOpt(name="bge-m3"),
        sparse_model=EmbeddingModelOpt(name="bge-m3"),
        data=[{"text": "generate dense & sparse embeddings with VikingDB"}],
    )
    response = embedding_client.embedding(request, request_options=request_options)
    assert response.result and response.result.data
    item = response.result.data[0]
    assert item.dense and len(item.dense) > 0