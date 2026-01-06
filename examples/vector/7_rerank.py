# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import json

from vikingdb import IAM
from vikingdb.vector import VikingVector, RerankRequest, FullModalData


def main() -> None:
    """Inline rerank call."""
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
    rerank_client = client.rerank()

    request = RerankRequest(
        model_name="doubao-seed-rerank",
        model_version="251028",
        data=[
            [FullModalData(text="Here is a mountain and it is very beautiful.")],
            [FullModalData(image="https://ark-project.tos-cn-beijing.volces.com/images/view.jpeg")],
            [FullModalData(video={"value": "https://ark-project.tos-cn-beijing.volces.com/doc_video/ark_vlm_video_input.mp4", "fps": 0.2})],
        ],
        query=[FullModalData(text="This is iceberg.")],
        instruction="Whether the Document answers the Query or matches the content retrieval intent",
        return_origin_data=True,
    )
    response = rerank_client.rerank(request)
    data = response.result.data if response.result and response.result.data else []
    print(f"Rerank request_id={response.request_id}")
    if hasattr(response, "model_dump"):
        try:
            print(response.model_dump_json(indent=2, by_alias=True) if hasattr(response, "model_dump_json") else json.dumps(response.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))
        except Exception:
            pass


if __name__ == "__main__":
    main()