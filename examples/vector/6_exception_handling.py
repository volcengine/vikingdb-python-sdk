# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""Scenario 6 – Exception handling for the vector client (main script).

This script demonstrates how to:
- Catch SDK-specific exceptions (e.g., VikingVectorException, VikingConnectionException)
- Inspect error codes and messages
- Print friendly outputs for troubleshooting

Run:
  python examples/vector/6_exception_handling.py
  python -m examples.vector.6_exception_handling
"""

from __future__ import annotations

import os

from vikingdb import IAM
from vikingdb.vector import SearchByRandomRequest, VikingDB


def main() -> None:
    """Connectivity quickstart mirroring the snippet test."""
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
    index_client = client.index(
        collection_name="unknown",
        index_name="unknown",
    )

    index_client.search_by_random(SearchByRandomRequest(limit=1))


if __name__ == "__main__":
    main()
