"""Scenario 6 – Exception handling for the vector client."""

from __future__ import annotations

import pytest

from vikingdb import IAM
from vikingdb.exceptions import NETWORK_ERROR_CODE
from vikingdb.vector import VikingVector
from vikingdb.vector.exceptions import VikingVectorException, VikingConnectionException

from .guide_helpers import EnvConfig, load_config


def _build_vector_client(*, host_override: str | None = None, timeout: int | None = None) -> tuple[EnvConfig, VikingVector]:
    """
    Create a VikingVector client using the shared guide configuration.

    ``host_override`` allows tests to force failure scenarios (for example, invalid hosts),
    while ``timeout`` lets them shorten request durations for network errors.
    """
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


def test_exception_collection_not_exist() -> None:
    """Calling a non-existent collection should surface a VikingVectorException with a helpful code."""
    config, client = _build_vector_client()
    missing_collection = f"{config.collection}-missing"

    collection_client = client.collection(
        collection_name=missing_collection,
        project_name=config.project_name,
        resource_id=config.resource_id,
    )

    with pytest.raises(VikingVectorException) as exc_info:
        collection_client.fetch({"ids": ["non-existent-id"]})

    error_code = str(exc_info.value.code)
    assert "NotFound" in error_code


def test_exception_wrong_host_raises_network() -> None:
    """Using an invalid host should raise a network exception promoted to VikingVectorException."""
    with pytest.raises(VikingConnectionException) as exc_info:
        _build_vector_client(host_override="in-v-alid.io", timeout=1)
    
    assert exc_info
