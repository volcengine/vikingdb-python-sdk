# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import json

from vikingdb import IAM
from vikingdb.vector import EmbeddingData, EmbeddingModelOpt, EmbeddingRequest, VikingVector


def main() -> None:
    """Inline dense+sparse embedding call."""
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
    embedding_client = client.embedding()

    request = EmbeddingRequest(
        dense_model=EmbeddingModelOpt(name="bge-m3"),
        sparse_model=EmbeddingModelOpt(name="bge-m3"),
        data=[EmbeddingData(text="Reference dense and sparse embedding request.")],
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