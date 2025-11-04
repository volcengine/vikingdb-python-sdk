# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Scenario 5 – Embedding Pipelines
"""
from __future__ import annotations

import os

import pytest

from vikingdb import IAM
from vikingdb.vector import EmbeddingData, EmbeddingModelOpt, EmbeddingRequest, FullModalData, VikingVector

from .guide_helpers import (
    Clients,
    build_clients,
    build_request_options,
    load_config,
    new_session_tag,
)


def test_snippet_embedding_multimodal_pipeline() -> None:
    """
    Inline multimodal embedding showcasing dense+sparse configuration.
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


def test_snippet_embedding_ds_pipeline() -> None:
    """
    Inline dense+sparse embedding call mirroring the Go DS snippet.
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


@pytest.fixture(scope="module")
def embedding_clients() -> Clients:
    return build_clients(load_config())


def test_scenario_embedding_multimodal_pipeline(embedding_clients: Clients) -> None:
    session_tag = new_session_tag("embedding-multimodal")
    request_options = build_request_options(session_tag)

    text = "generate embeddings with VikingDB"
    request = EmbeddingRequest(
        dense_model=EmbeddingModelOpt(name="doubao-embedding-vision", version="250615"),
        sparse_model=EmbeddingModelOpt(name="bge-m3"),
        data=[
            EmbeddingData(
                full_modal_seq=[FullModalData(text=text)],
            )
        ],
    )
    response = embedding_clients.embedding.embedding(request, request_options=request_options)
    assert response.result and response.result.data
    item = response.result.data[0]
    assert item.dense and len(item.dense) > 0


def test_scenario_embedding_ds_pipeline(embedding_clients: Clients) -> None:
    session_tag = new_session_tag("embedding-ds")
    request_options = build_request_options(session_tag)

    request = EmbeddingRequest(
        dense_model=EmbeddingModelOpt(name="bge-m3"),
        sparse_model=EmbeddingModelOpt(name="bge-m3"),
        data=[EmbeddingData(text="generate dense & sparse embeddings with VikingDB")],
    )
    response = embedding_clients.embedding.embedding(request, request_options=request_options)
    assert response.result and response.result.data
    item = response.result.data[0]
    assert item.dense and len(item.dense) > 0
