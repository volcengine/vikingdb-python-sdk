# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import json

from vikingdb import IAM
from vikingdb.vector import EmbeddingData, EmbeddingModelOpt, EmbeddingRequest, FullModalData, VikingDB


def main() -> None:
    """Inline multimodal embedding showcasing dense+sparse configuration."""
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
    embedding_client = client.embedding()

    text = "Short multimodal prompt for the reference embedding pipeline."
    request = EmbeddingRequest(
        dense_model=EmbeddingModelOpt(name="doubao-embedding-vision", version="250615"),
        sparse_model=EmbeddingModelOpt(name="bge-m3"),
        data=[
            EmbeddingData(
                full_modal_seq=[FullModalData(text=text)],
            )
        ],
    )
    response = embedding_client.embedding(request)
    data = response.result.data if response.result and response.result.data else []
    dims = len(data[0].dense) if data and data[0].dense else 0
    print(f"Embedding request_id={response.request_id} dense_dims={dims}")
    if hasattr(response, "model_dump"):
        try:
            print(response.model_dump_json(indent=2, by_alias=True) if hasattr(response, "model_dump_json") else json.dumps(response.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))
        except Exception:
            pass


if __name__ == "__main__":
    main()