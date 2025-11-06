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

import sys

from vikingdb import IAM
from vikingdb.vector import VikingVector
from vikingdb.vector.exceptions import VikingVectorException, VikingConnectionException

from .test_helper import EnvConfig, load_config


def _build_vector_client(*, host_override: str | None = None, timeout: int | None = None) -> tuple[EnvConfig, VikingVector]:
    """Create a VikingVector client using the shared guide configuration."""
    config = load_config()
    auth = IAM(ak=config.access_key, sk=config.secret_key)
    client = VikingVector(
        host=host_override if host_override is not None else config.host,
        region=config.region,
        scheme=config.scheme,
        auth=auth,
        timeout=timeout if timeout is not None else 30,
    )
    return config, client


def demo_collection_not_exist() -> None:
    """Attempt to fetch from a non-existent collection to trigger an SDK exception."""
    try:
        config, client = _build_vector_client()
        missing_collection = f"{config.collection}-missing"
        collection_client = client.collection(
            collection_name=missing_collection,
            project_name=config.project_name,
            resource_id=config.resource_id,
        )
        # Intentionally request a fake ID
        collection_client.fetch({"ids": ["non-existent-id"]})
    except VikingVectorException as e:
        print(f"Caught VikingVectorException: code={getattr(e, 'code', None)} message={e}")


def demo_wrong_host_network_error() -> None:
    """Use an invalid host to demonstrate a network connection error."""
    try:
        _build_vector_client(host_override="in-v-alid.io", timeout=1)
    except VikingConnectionException as e:
        print(f"Caught VikingConnectionException: message={e}")



def main() -> int:
    print("-- Scenario 6: Exception handling demos --")
    demo_collection_not_exist()
    demo_wrong_host_network_error()
    print("-- Done --")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
