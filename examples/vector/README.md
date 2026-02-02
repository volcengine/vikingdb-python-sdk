# VikingDB Python Example Guides

The `examples/vector` package provides executable guides mirroring the richer walkthroughs you liked, now aligned with the current SDK. Each scenario can be run as a standalone script or via pytest.

## Quickstart Walkthrough

The snippet below mirrors the connectivity flow without helper imports. Populate environment variables (or a `.env` file) before running.

```python
import os
from vikingdb import IAM
from vikingdb.vector import SearchByRandomRequest, VikingDB

auth = IAM(ak=os.environ["VIKINGDB_AK"], sk=os.environ["VIKINGDB_SK"]) 
client = VikingDB(
    host=os.environ["VIKINGDB_HOST"],
    region=os.environ["VIKINGDB_REGION"],
    auth=auth,
    scheme="https",
    timeout=30,
)
index = client.index(
    collection_name=os.environ["VIKINGDB_COLLECTION"],
    index_name=os.environ["VIKINGDB_INDEX"],
)
resp = index.search_by_random(SearchByRandomRequest(limit=1))
print(f"request_id={resp.request_id} hits={len(resp.result.data or [])}")
```

## Running the Guides

Requires a `.env` file with credentials and defaults. Use the following pattern to run main scripts:

- Connectivity:
  - env $(grep -v '^#' .env | xargs) uv run examples/vector/1_connectivity.py
- Collection lifecycle:
  - env $(grep -v '^#' .env | xargs) uv run examples/vector/2_collection_lifecycle.py
- Index search (multimodal):
  - env $(grep -v '^#' .env | xargs) uv run examples/vector/3_1_index_search_multimodal.py
- Index search (vector):
  - env $(grep -v '^#' .env | xargs) uv run examples/vector/3_2_index_search_vector.py
- Search by keyword:
  - env $(grep -v '^#' .env | xargs) uv run examples/vector/3_3_search_by_keyword.py
- Search + aggregate:
  - env $(grep -v '^#' .env | xargs) uv run examples/vector/4_search_aggregate.py
- Embedding (multimodal):
  - env $(grep -v '^#' .env | xargs) uv run examples/vector/5_1_embedding_multimodal.py
- Embedding (ds pipeline):
  - env $(grep -v '^#' .env | xargs) uv run examples/vector/5_2_embedding_ds.py
- Exception handling:
  - env $(grep -v '^#' .env | xargs) uv run examples/vector/6_exception_handling.py

Run with pytest:

```bash
# run all scenario tests with assertions
env $(grep -v '^#' .env | xargs) pytest -q examples/vector -k scenario
# focus on inline snippets (embedding dataset)
env $(grep -v '^#' .env | xargs) pytest -q examples/vector -k "test_snippet"
# run the vector-only snippets
env $(grep -v '^#' .env | xargs) pytest -q examples/vector -k "test_v_snippet"
```

### Environment Variables

| Variable                      | Purpose                                  |
|------------------------------|------------------------------------------|
| `VIKINGDB_AK` / `VIKINGDB_SK`| IAM access keys used for signing requests |
| `VIKINGDB_HOST`              | Fully qualified API hostname (no scheme)  |
| `VIKINGDB_REGION`            | Region used for signing and routing       |
| `VIKINGDB_COLLECTION`        | Default collection for collection/index APIs |
| `VIKINGDB_INDEX`             | Default index for search-focused guides   |

Populate these via a `.env` file or exported variables before running. The scenario flows default to public demo datasets, but AK/SK are always required.

#### Switching datasets

The public guides run against two collections:

- Embedding dataset (default): `VIKINGDB_COLLECTION=text`, `VIKINGDB_INDEX=text_index`
- Vector-only dataset: `VIKINGDB_COLLECTION=vector`, `VIKINGDB_INDEX=vector_index`

Override per-run values inline:

```bash
# embedding dataset
env $(grep -v '^#' .env | xargs) pytest -q examples/vector -k "test_snippet"

# vector dataset (overrides collection/index for this invocation)
env $(grep -v '^#' .env | xargs) \
  VIKINGDB_COLLECTION=vector \
  VIKINGDB_INDEX=vector_index \
  pytest -q examples/vector -k "test_v_snippet"
```

## Scenario Overview

| Guide     | Script                           | What it demonstrates                                                                 | Key SDK calls                                                |
|-----------|----------------------------------|---------------------------------------------------------------------------------------|--------------------------------------------------------------|
| Guide 1   | `1_connectivity.py`              | Bootstrap SDK clients and validate connectivity via `search_by_random`.               | `VikingDB`, `index`, `IndexClient.search_by_random`      |
| Guide 2   | `2_collection_lifecycle.py`      | Full CRUD lifecycle for Atlas chapters, including ID hydration through search.        | `collection.upsert`, `index.search_by_multi_modal`, `collection.update/fetch/delete` |
| Guide 3.1 | `3_1_index_search_multimodal.py` | Multi-modal search with scalar filters scoped to the current session.                 | `collection.upsert`, `index.search_by_multi_modal`           |
| Guide 3.2 | `3_2_index_search_vector.py`     | Pure vector search with index-side ingestion and querying.                            | `embedding.embedding`, `index.search_by_vector`              |
| Guide 3.3 | `3_3_search_by_keyword.py`       | Keyword search across text fields with limit and field selection.                     | `index.search_by_keywords`                                   |
| Guide 4   | `4_search_aggregate.py`          | Aggregations over search results (count) filtered by session-scoped chapter selection.| `index.aggregate`                                            |
| Guide 5.1 | `5_1_embedding_multimodal.py`    | Multimodal embedding pipeline usage with text+image payloads.                         | `embedding.embedding`                                        |
| Guide 5.2 | `5_2_embedding_ds.py`            | Data source embedding pipeline usage across the public dataset.                        | `embedding.embedding`                                        |

### SDK API Coverage

`X` indicates the API is exercised by the corresponding guide.

| SDK API                             | Client       | G1 | G2 | G3.1 | G3.2 | G3.3 | G4 | G5 |
|-------------------------------------|--------------|----|----|------|------|------|----|----|
| `VikingDB`                      | Vector       | X  | X  | X    | X    | X    | X  | X  |
| `Client.collection`                 | Vector       |    | X  | X    | X    | X    | X  |    |
| `Client.index`                      | Vector       | X  | X  | X    | X    | X    | X  |    |
| `Client.embedding`                  | Vector       | X  |    |      | X    |      |    | X  |
| `CollectionClient.upsert`           | Collection   |    | X  | X    | X    | X    | X  |    |
| `CollectionClient.update`           | Collection   |    | X  |      |      |      |    |    |
| `CollectionClient.delete`           | Collection   |    | X  |      |      |      |    |    |
| `CollectionClient.fetch`            | Collection   |    | X  |      |      |      |    |    |
| `IndexClient.search_by_vector`      | Index        |    |    |      | X    |      |    |    |
| `IndexClient.search_by_multi_modal` | Index        |    | X  | X    |      |      |    |    |
| `IndexClient.search_by_keywords`    | Index        |    |    |      |      | X    |    |    |
| `IndexClient.search_by_random`      | Index        | X  |    |      |      |      |    |    |
| `IndexClient.aggregate`             | Index        |    |    |      |      |      | X  |    |
| `EmbeddingClient.embedding`         | Embedding    |    |    |      | X    |      |    | X  |

### Uncovered Areas

- Index-level fetch, ID lookup, and scalar-only search (`search_by_id`, `search_by_scalar`) are not yet represented.
- API-key constructors remain unillustrated; all examples authenticate with AK/SK credentials.
- Video & Image MultiModal Search
- Video & Image Embedding
