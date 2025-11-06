# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import time
import json

from vikingdb import IAM
from vikingdb.vector import (
    EmbeddingModelOpt,
    EmbeddingRequest,
    SearchByVectorRequest,
    UpsertDataRequest,
    VikingVector,
)


def _to_float_list(vector) -> list[float]:
    if not vector:
        return []
    return [float(v) for v in vector]


def main() -> None:
    """Inline vector search: embed chapters → write vectors → embed query → SearchByVector."""
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
    # Pretty print embedding response
    if hasattr(embed_resp, "model_dump"):
        try:
            print(embed_resp.model_dump_json(indent=2, by_alias=True) if hasattr(embed_resp, "model_dump_json") else json.dumps(embed_resp.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))
        except Exception:
            pass
    dense_vectors = [_to_float_list(item.dense) for item in embed_resp.result.data]

    payload = []
    for chapter, vector in zip(chapters, dense_vectors):
        payload.append({**chapter, "vector": vector})
    collection_client.upsert(UpsertDataRequest(data=payload))

    time.sleep(2)

    query_req = EmbeddingRequest(
        data=[{"text": "Show me the chapter that demonstrates embedding reuse for query vectors."}],
        dense_model=EmbeddingModelOpt(name="bge-m3"),
    )
    query_resp = embedding_client.embedding(query_req)
    assert query_resp.result and query_resp.result.data
    # Pretty print query embedding response
    if hasattr(query_resp, "model_dump"):
        try:
            print(query_resp.model_dump_json(indent=2, by_alias=True) if hasattr(query_resp, "model_dump_json") else json.dumps(query_resp.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))
        except Exception:
            pass
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
    if hasattr(response, "model_dump"):
        try:
            print(response.model_dump_json(indent=2, by_alias=True) if hasattr(response, "model_dump_json") else json.dumps(response.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))
        except Exception:
            pass


if __name__ == "__main__":
    main()