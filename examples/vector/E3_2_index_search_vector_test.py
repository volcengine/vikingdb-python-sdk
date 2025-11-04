# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Scenario 3.2 – Vector Retrieval With Embeddings
"""
from __future__ import annotations

import time
import pytest
import os

from vikingdb import IAM
from vikingdb.vector import (
    EmbeddingModelOpt,
    EmbeddingRequest,
    SearchByVectorRequest,
    UpsertDataRequest,
    VikingDB,
)

from .guide_helpers import (
    VECTOR_COLLECTION,
    VECTOR_INDEX,
    Clients,
    build_clients,
    build_request_options,
    embed_dense_vectors,
    load_config,
    new_session_tag,
    session_paragraph_bounds,
    build_story_chapters,
    cleanup_chapters,
)


def _to_float_list(vector) -> list[float]:
    if not vector:
        return []
    return [float(v) for v in vector]


def test_v_snippet_index_search_vector() -> None:
    """
    Inline vector search that mirrors the Go snippet: embed chapters, write them with vectors,
    embed a query, then run SearchByVector.
    """
    client = VikingDB(
        endpoint=f"https://{os.environ['VIKINGDB_HOST']}",
        region=os.environ["VIKINGDB_REGION"],
        timeout=30.0,
        user_agent="vikingdb-python-sdk-guide",
        auth=IAM(os.environ["VIKINGDB_AK"], os.environ["VIKINGDB_SK"]),
    )
    collection_client = client.collection(collection_name=os.environ["VIKINGDB_COLLECTION"])
    index_client = client.index(
        collection_name=os.environ["VIKINGDB_COLLECTION"],
        index_name=os.environ["VIKINGDB_INDEX"],
    )
    embedding_client = client.embedding()

    base_paragraph = int(time.time() * 1e6) % 1_000_000
    chapters = [
        {"title": "Vector intro", "paragraph": base_paragraph, "score": 80.0, "text": "Inline vector search example."},
        {
            "title": "Vector deep dive",
            "paragraph": base_paragraph + 1,
            "score": 81.0,
            "text": "Demonstrates embedding reuse for query vectors.",
        },
    ]

    embed_req = EmbeddingRequest(
        data=[{"text": chapter["text"]} for chapter in chapters],
        dense_model=EmbeddingModelOpt(name="bge-m3"),
    )
    embed_resp = embedding_client.embedding(embed_req)
    if not embed_resp.result or not embed_resp.result.data:
        print("Embedding response missing data")
        return
    dense_vectors = [_to_float_list(item.dense) for item in embed_resp.result.data]

    payload = []
    for chapter, vector in zip(chapters, dense_vectors):
        payload.append({**chapter, "vector": vector})
    collection_client.upsert(UpsertDataRequest(data=payload))

    time.sleep(3)

    query_req = EmbeddingRequest(
        data=[{"text": "Show me the chapter that demonstrates embedding reuse for query vectors."}],
        dense_model=EmbeddingModelOpt(name="bge-m3"),
    )
    query_resp = embedding_client.embedding(query_req)
    assert query_resp.result and query_resp.result.data
    query_vector = _to_float_list(query_resp.result.data[0].dense)

    filter_map = {"op": "range", "field": "paragraph", "gte": base_paragraph, "lt": base_paragraph + len(chapters)}
    search_req = SearchByVectorRequest(
        dense_vector=query_vector,
        limit=3,
        output_fields=["title", "score", "paragraph"],
        filter=filter_map,
    )
    response = index_client.search_by_vector(search_req)
    hits = response.result.data if response.result and response.result.data else []
    print(f"SearchByVector request_id={response.request_id} hits={len(hits)}")


@pytest.fixture(scope="module")
def vector_clients() -> Clients:
    config = load_config(collection=VECTOR_COLLECTION, index=VECTOR_INDEX)
    return build_clients(config)


def test_scenario_index_search_vector(vector_clients: Clients) -> None:
    session_tag = new_session_tag("search-vector")
    request_options = build_request_options(session_tag)
    base_paragraph = int(time.time()) % 1_000_000
    chapters = build_story_chapters(session_tag, base_paragraph)

    try:
        chapter_vectors = embed_dense_vectors(
            vector_clients.embedding,
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
        vector_clients.collection.upsert(UpsertDataRequest(data=payload), request_options=request_options)

        time.sleep(3)

        retrieval = next(ch for ch in chapters if ch.key == "retrieval-lab")
        query_vector = embed_dense_vectors(
            vector_clients.embedding,
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
        response = vector_clients.index.search_by_vector(search_req, request_options=request_options)
        assert response.result and response.result.data
        titles = [hit.fields.get("title") for hit in response.result.data]
        assert retrieval.title in titles
    finally:
        cleanup_chapters(vector_clients.collection, chapters, request_options=request_options)
