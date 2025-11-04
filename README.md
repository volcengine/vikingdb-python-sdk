## VikingDB Python SDK (v2)

This package provides an idiomatic Python interface to the VikingDB v2 data-plane APIs. The SDK mirrors the behaviour and API surface of the official Java and Go clients while embracing Python conventions (dataclasses/pydantic models, requests-based transport, and pytest-driven examples).

### Key Features
- Shared client configuration with AK/SK signing (Volcano Engine V4) or API-key authentication.
- Request envelope handling with typed request/response models covering collection, index, and embedding workflows.
- Pluggable retry strategy (exponential backoff with jitter) and per-request overrides (`RequestOptions`).
- Executable example guides (`pytest` integration tests) that demonstrate connectivity, CRUD, search, analytics, and embedding scenarios against a real VikingDB environment.

### Installation

Clone the repository and install the SDK in editable mode:

```bash
pip install -e .
```

> **Dependencies:** The SDK relies on `requests`, `pydantic>=2.5`, and the Volcano Engine base SDK (`volcengine`) for request signing.

### Quickstart

```python
from vikingdb import IAM
from vikingdb.vector import UpsertDataRequest, VikingDB

client = VikingDB(
    endpoint="https://api.vector.bytedance.com",
    region="cn-beijing",
    timeout=30.0,
    user_agent="vikingdb-python-sdk-demo",
    auth=IAM("<AK>", "<SK>"),
)

collection = client.collection(collection_name="demo_collection")
index = client.index(collection_name="demo_collection", index_name="demo_index")
embedding = client.embedding()

# Upsert documents into a collection
upsert_request = UpsertDataRequest(
    data=[
        {"title": "Demo Chapter", "paragraph": 1, "score": 42.0, "text": "hello vikingdb"},
    ]
)
response = collection.upsert(upsert_request)
print("request_id:", response.request_id, "result:", response.result)

# Run a quick search
search_response = index.search_by_random({"limit": 1})
print("search hits:", len(search_response.result.data) if search_response.result else 0)
```

### Example Guides (Pytest)

The integration guides under `examples/vector` mirror the Go SDK walkthroughs (`E1`–`E5`). Each test connects to a live VikingDB environment and exercises a specific workflow.

1. Set the required environment variables (or create a `.env` file in the project root):

   ```
   VIKINGDB_AK=your-access-key
   VIKINGDB_SK=your-secret-key
   # Optional:
   # VIKINGDB_PROJECT=project-name
   # VIKINGDB_RESOURCE_ID=resource-id
   ```

   The pytest guides themselves lock to the ap-southeast-1 public datasets:

   - host: `api-vikingdb.vikingdb.ap-southeast-1.volces.com`
   - region: `ap-southeast-1`
   - text walkthroughs use `collection=text`, `index=text_index`
   - vector walkthroughs use `collection=vector`, `index=vector_index`

2. Install pytest (if not already available):

   ```bash
   pip install pytest
   ```

3. Execute the guides:

   ```bash
   pytest examples/vector -k guide
   ```

Each scenario writes temporary documents using unique session tags and cleans them up afterwards.

### Architecture Overview

- `vikingdb.config`, `vikingdb.credentials`, `vikingdb.transport`, `vikingdb.request_options`, and `vikingdb.exceptions` form the shared runtime used by all present and future SDK domains (vector, memory, knowledge).
- Domain-specific features live under dedicated namespaces such as `vikingdb.vector`, where the high-level `VikingDB` client composes the shared transport/auth stack.
- Vector request/response models now surface directly from `vikingdb.vector` (backed internally by `vikingdb/vector/models`).
- Imports from the root package now focus on cross-cutting utilities (auth, config, request options), while application code should pull vector functionality from `vikingdb.vector` explicitly.

### Project Structure

```
vikingdb/
├── config.py            # Shared client / retry configuration
├── credentials.py       # AK/SK and API-key auth strategies
├── exceptions.py        # Error hierarchy reused across domains
├── request_options.py   # Per-request overrides shared by all services
├── transport.py         # HTTP executor with retries and auth
├── version.py           # Package metadata
├── vector/              # Vector-specific clients and models
│   ├── __init__.py      # High-level vector client and namespace exports
│   ├── base.py          # Shared helpers for vector clients
│   ├── collection.py    # Collection operations
│   ├── embedding.py     # Embedding operations
│   ├── index.py         # Index/search operations
│   └── models/          # Vector request/response models (pydantic)

examples/vector/         # Integration guides (pytest)
docs/python_sdk_design.md# Design notes and parity checklist
```

### Contributing

Contributions and feedback are welcome. Please ensure any new APIs match the OpenAPI specification and include accompanying example coverage.
