# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Scenario 1 – Connecting to VikingDB

Mirrors the Go guide by shipping two pytest flows:
  * ``test_snippet_connectivity`` keeps the setup inline for quick copy/paste.
  * ``test_scenario_connectivity`` reuses the shared helpers to validate connectivity.
"""
from __future__ import annotations

import os
import pytest

from vikingdb import IAM
from vikingdb.vector import SearchByRandomRequest, VikingDB

from .guide_helpers import (
    Clients,
    build_clients,
    build_request_options,
    load_config,
    new_session_tag,
)


def test_snippet_connectivity() -> None:
    """
    Inline connectivity check. Export the following variables before running:

        VIKINGDB_AK=...
        VIKINGDB_SK=...
        VIKINGDB_HOST=...
        VIKINGDB_REGION=...
        VIKINGDB_COLLECTION=...
        VIKINGDB_INDEX=...
    """
    client = VikingDB(
        endpoint=f"https://{os.environ['VIKINGDB_HOST']}",
        region=os.environ["VIKINGDB_REGION"],
        timeout=30.0,
        user_agent="vikingdb-python-sdk-guide",
        auth=IAM(os.environ["VIKINGDB_AK"], os.environ["VIKINGDB_SK"]),
    )
    index_client = client.index(
        collection_name=os.environ["VIKINGDB_COLLECTION"],
        index_name=os.environ["VIKINGDB_INDEX"],
    )

    response = index_client.search_by_random(SearchByRandomRequest(limit=1))
    data = []
    if response.result and response.result.data:
        data = response.result.data
    hits = len(data)
    print(f"SearchByRandom request_id={response.request_id} hits={hits}")


@pytest.fixture(scope="module")
def clients() -> Clients:
    return build_clients(load_config())


def test_scenario_connectivity(clients: Clients) -> None:
    session_tag = new_session_tag("scenario-connectivity")
    request_options = build_request_options(session_tag)
    response = clients.index.search_by_random(SearchByRandomRequest(limit=1), request_options=request_options)
    assert response.request_id
    assert clients.collection is not None
    assert clients.embedding is not None
    hits = 0 if not response.result or not response.result.data else len(response.result.data)
    print(
        f"Connectivity check host={os.getenv('VIKINGDB_HOST', 'default-host')} "
        f"region={os.getenv('VIKINGDB_REGION', 'default-region')} "
        f"request_id={response.request_id} hits={hits}"
    )
