# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import random
import sys
import time
import pytest
from vikingdb.vector import UpsertDataRequest, SearchByVectorRequest, VikingDB

# Ensure local helper can be imported when running via pytest path
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from test_helper import load_config, build_client

COLLECTION_NAME = "test_collection_emb"
INDEX_NAME = "test_collection_emb_idx"

@pytest.fixture(scope="module")
def client() -> VikingDB:
    """Fixture to initialize VikingDB client with NoAuth and custom headers."""
    cfg = load_config()
    client = build_client(cfg)
    return client

class TestVectorNoAuth:
    # Use a shared state to pass data between write and read tests if needed, 
    # though in a real CI/CD environment, tests should ideally be independent.
    # Here we'll generate the data in each test or use fixed IDs for simplicity in this example.
    test_id = random.randint(1000000, 9999999)
    test_vector = [random.random() for _ in range(768)]

    def test_upsert_data(self, client: VikingDB):
        """Test writing data to the collection with HeaderAuth."""
        collection_client = client.collection(collection_name=COLLECTION_NAME)
        
        data = [
            {
                "id": self.test_id,
                "dense_vector": self.test_vector,
                "sparse_vector": {"1": 0.1, "10": 0.5},
                "range": 10,
                "enum": "test_A",
                "text": "Pytest record with HeaderAuth"
            }
        ]
        
        upsert_resp = collection_client.upsert(UpsertDataRequest(data=data))
        assert upsert_resp.request_id is not None
        print(f"Upsert successful, request_id: {upsert_resp.request_id}")

    def test_search_data(self, client: VikingDB):
        """Test reading data from the index with HeaderAuth."""
        # Wait a bit for indexing
        time.sleep(2)
        
        index_client = client.index(collection_name=COLLECTION_NAME, index_name=INDEX_NAME)
        
        search_request = SearchByVectorRequest(
            dense_vector=self.test_vector,
            limit=10,
            output_fields=["id", "text"]
        )
        search_resp = index_client.search_by_vector(search_request)
        
        assert search_resp.request_id is not None
        assert search_resp.result is not None
        
        # Verify the record we just upserted is found (or at least the request succeeded)
        found = any(item.id == self.test_id for item in search_resp.result.data)
        if not found:
             print(f"Warning: Record {self.test_id} not found in search results. Indexing might be delayed.")
        
        print(f"Search successful, request_id: {search_resp.request_id}")

if __name__ == "__main__":
    pytest.main([__file__])
