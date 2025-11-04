# VikingDB Python Example Guides

The `examples/vector` package mirrors the Go SDK's executable guides using pytest. Each `E*`
module ships two flows:

- `test_snippet_*` keeps all request payloads inline so you can copy/paste them into notebooks.
- `test_scenario_*` reuses shared helpers to produce richer walkthroughs that double as smoke tests.

## Quickstart Walkthrough

The snippet below mirrors `test_snippet_connectivity` without any helper imports. Export the
environment variables in a shell (or populate `.env`) before running the test.

```python
import os
from vikingdb import IAM
from vikingdb.vector import SearchByRandomRequest, VikingDB

client = VikingDB(
    endpoint=f"https://{os.environ['VIKINGDB_HOST']}",
    region=os.environ["VIKINGDB_REGION"],
    timeout=30.0,
    user_agent="vikingdb-python-sdk-guide",
    auth=IAM(os.environ["VIKINGDB_AK"], os.environ["VIKINGDB_SK"]),
)
index = client.index(
    collection_name=os.environ["VIKINGDB_COLLECTION"],
    index_name=os.environ["VIKINGDB_INDEX"],
)
response = index.search_by_random(SearchByRandomRequest(limit=1))
print(f"request_id={response.request_id} hits={len(response.result.data or [])}")
```

Once this passes, explore the richer pytest scenarios.

## Running the Guides

```bash
# run all scenario tests with assertions
pytest -q examples/vector -k scenario
# focus on inline snippets (embeddings dataset)
env $(grep -v '^#' .env | xargs) pytest -q examples/vector -k "test_snippet"
# run the vector-only snippets
env $(grep -v '^#' .env | xargs) pytest -q examples/vector -k "test_v_snippet"
```

### Environment Variables

| Variable                        | Purpose                                           |
|---------------------------------|---------------------------------------------------|
| `VIKINGDB_AK` / `VIKINGDB_SK`   | IAM access keys used for signing requests.        |
| `VIKINGDB_HOST`                 | Fully qualified API hostname (no scheme).         |
| `VIKINGDB_REGION`               | Region used for signing and routing.              |
| `VIKINGDB_COLLECTION`           | Default collection for collection/index APIs.     |
| `VIKINGDB_INDEX`                | Default index for search-focused guides.          |

Populate them via environment variables or a `.env` file before running pytest. The scenario tests
fall back to the public demo datasets documented in the Python SDK guide, but AK/SK are always required.

#### Switching datasets

The public guides run against two collections:

- **Embedding dataset** (default): `VIKINGDB_COLLECTION=text`, `VIKINGDB_INDEX=text_index`
- **Vector-only dataset**: `VIKINGDB_COLLECTION=vector`, `VIKINGDB_INDEX=vector_index`

Update the `.env` file (or exported variables) before running the vector-only tests:

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

| Guide     | Test (module)                       | What it demonstrates                                                                 | Key SDK calls                                                                                             |
|-----------|-------------------------------------|----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Guide 1   | `E1_connectivity_test.py`           | Bootstrap SDK clients and validate connectivity via `search_by_random`.                | `VikingDB`, `Client.index`, `IndexClient.search_by_random`                                                |
| Guide 2   | `E2_collection_lifecycle_test.py`   | Full CRUD lifecycle for Atlas chapters, including ID hydration through search.         | `CollectionClient.upsert`, `IndexClient.search_by_multi_modal`, `CollectionClient.update/fetch/delete`    |
| Guide 3.1 | `E3_1_index_search_multimodal_test.py` | Multi-modal search with scalar filters scoped to the current session.                  | `CollectionClient.upsert`, `IndexClient.search_by_multi_modal`                                            |
| Guide 3.2 | `E3_2_index_search_vector_test.py`  | Dense vector retrieval with filter windows and embedding reuse.                        | `EmbeddingClient.embedding`, `CollectionClient.upsert`, `IndexClient.search_by_vector`                    |
| Guide 3.3 | `E3_3_search_by_keyword_test.py`    | Keyword-driven retrieval focused on tagged Atlas chapters.                              | `CollectionClient.upsert`, `IndexClient.search_by_keywords`                                               |
| Guide 4   | `E4_search_aggregate_test.py`       | Aggregate analytics over the active session's chapters.                                | `CollectionClient.upsert`, `IndexClient.aggregate`                                                        |
| Guide 5   | `E5_embedding_test.py`              | Multimodal and dense+sparse embedding requests with token usage inspection.            | `EmbeddingClient.embedding`                                                                               |

### SDK API Coverage

`X` indicates the API is exercised by the corresponding guide.

| SDK API                           | Client      | E1 | E2 | E3.1 | E3.2 | E3.3 | E4 | E5 |
|-----------------------------------|-------------|----|----|------|------|------|----|----|
| `VikingDB`                        | VikingDB    | X  | X  | X    | X    | X    | X  | X  |
| `Client.collection`               | VikingDB    |    | X  | X    | X    | X    | X  |    |
| `Client.index`                    | VikingDB    | X  | X  | X    | X    | X    | X  |    |
| `Client.embedding`                | VikingDB    | X  |    |      | X    |      |    | X  |
| `CollectionClient.upsert`         | Collection  |    | X  | X    | X    | X    | X  |    |
| `CollectionClient.update`         | Collection  |    | X  |      |      |      |    |    |
| `CollectionClient.delete`         | Collection  |    | X  |      |      |      |    |    |
| `CollectionClient.fetch`          | Collection  |    | X  |      |      |      |    |    |
| `IndexClient.search_by_vector`    | Index       |    |    |      | X    |      |    |    |
| `IndexClient.search_by_multi_modal` | Index     |    | X  | X    |      |      |    |    |
| `IndexClient.search_by_keywords`  | Index       |    |    |      |      | X    |    |    |
| `IndexClient.search_by_random`    | Index       | X  |    |      |      |      |    |    |
| `IndexClient.aggregate`           | Index       |    |    |      |      |      | X  |    |
| `EmbeddingClient.embedding`       | Embedding   |    |    |      | X    |      |    | X  |

### Uncovered Areas

- Index-level fetch, ID lookup, and scalar-only search (`search_by_id`, `search_by_scalar`) are not yet represented.
- API-key constructors remain unillustrated; all examples authenticate with AK/SK credentials.
- Video & Image MultiModal Search
- Video & Image Embedding