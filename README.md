## VikingDB Python SDK (v2)

This package provides an idiomatic Python interface to the VikingDB v2 data-plane APIs. The SDK mirrors the behaviour and API surface of the official Java and Go clients while embracing Python conventions (dataclasses/pydantic models, requests-based transport, and pytest-driven examples).

### Key Features
- Simple client configuration with AK/SK signing (Volcano Engine V4) or API-key authentication.
- **Vector Database**: Request envelope handling with typed request/response models covering collection, index, and embedding workflows.
- **Memory Management**: Conversational memory APIs for managing user profiles, events, and session messages with semantic search capabilities.
- Pluggable retry strategy (exponential backoff with jitter) and per-request overrides (`RequestOptions`).
- Executable example guides (`pytest` integration tests and standalone scripts) that demonstrate connectivity, CRUD, search, analytics, embedding, and memory management scenarios against a real VikingDB environment.

### Installation

Clone the repository and install the SDK in editable mode:

```bash
uv add vikingdb-python-sdk
```

> **Dependencies:** The SDK relies on `requests`, `pydantic>=2.5`, and the Volcano Engine base SDK (`volcengine`) for request signing.

### Quickstart

#### Vector Database

```python
import os
from vikingdb import IAM
from vikingdb.vector import SearchByRandomRequest, VikingVector

auth = IAM(ak=os.environ["VIKINGDB_AK"], sk=os.environ["VIKINGDB_SK"]) 
client = VikingVector(
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

#### Memory Management

```python
from vikingdb import IAM
from vikingdb.memory import VikingMem

auth = IAM(ak="<AK>", sk="<SK>")
client = VikingMem(
    host="api-knowledgebase.mlp.cn-beijing.volces.com",
    region="cn-beijing",
    auth=auth,
    scheme="http",
)

# Get collection
collection = client.get_collection(
    collection_name="demo_collection",
    project_name="default"
)

# Add session messages
collection.add_session(
    session_id="session_001",
    messages=[
        {"role": "user", "content": "Hello, how is the weather today?"},
        {"role": "assistant", "content": "Today is sunny, perfect for going out."}
    ],
    metadata={
        "default_user_id": "user_001",
        "default_assistant_id": "assistant_001",
    }
)

# Search memories
result = collection.search_memory(
    query="weather today",
    filter={"user_id": "user_001", "memory_type": ["event_v1"]},
    limit=10
)
print("search results:", result)
```

### Example Guides

#### Vector Examples

The integration guides under `examples/vector` mirror the Go SDK walkthroughs (`1`–`6`). Each test connects to a live VikingDB environment and exercises a specific workflow.

1. Set the required environment variables (or create a `.env` file in the project root):

   ```
   VIKINGDB_AK=your-access-key
   VIKINGDB_SK=your-secret-key
   VIKINGDB_COLLECTION=demo_collection
   VIKINGDB_INDEX=demo_index
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
   uv add --dev pytest
   ```

3. Execute the guides:

   ```bash
   uv run pytest examples/vector -k scenario
   ```

Each scenario writes temporary documents using unique session tags and cleans them up afterwards.

#### Memory Examples

The memory examples under `examples/memory` demonstrate the core workflows for managing conversational memories:

1. **01_init_client_and_collection.py**: Initialize the VikingMem client and get collection instances using either collection name + project name or resource ID.

2. **02_add_session.py**: Add session messages (user-assistant conversations) to the memory collection with metadata such as user ID, assistant ID, and timestamps.

3. **03_search_memory.py**: Search memories with various filters including:
   - User profile search
   - Event search by semantic query
   - Time range filtering for recent events

To run the memory examples:

```bash
# Set environment variables
export VIKINGDB_AK=your-access-key
export VIKINGDB_SK=your-secret-key

# Run individual examples
python examples/memory/01_init_client_and_collection.py
python examples/memory/02_add_session.py
python examples/memory/03_search_memory.py
```

### Architecture Overview

- `vikingdb._client`, `vikingdb.auth`, `vikingdb.request_options`, and `vikingdb.vector.exceptions` form the shared runtime used by all present and future SDK domains (vector, memory, knowledge).
- Domain-specific features live under dedicated namespaces such as `vikingdb.vector` and `vikingdb.memory`, where the high-level clients (`VikingVector`, `VikingMem`) compose the shared auth stack atop the shared client.
- Vector request/response models now surface directly from `vikingdb.vector` (backed internally by `vikingdb/vector/models`).
- Memory APIs return plain dictionaries without object encapsulation, providing a lightweight interface for conversational memory management (session, profile, event operations).
- Imports from the root package now focus on cross-cutting utilities (auth, config, request options), while application code should pull domain-specific functionality from `vikingdb.vector` or `vikingdb.memory` explicitly.

### Project Structure

```
vikingdb/
├── _client.py          # Shared base client built on volcengine Service
├── auth.py              # Shared auth providers (IAM, API key)
├── request_options.py   # Per-request overrides shared by all services
├── version.py           # Package metadata
├── vector/              # Vector-specific clients and models
│   ├── __init__.py      # High-level vector client and namespace exports
│   ├── base.py          # Shared helpers for vector clients
│   ├── collection.py    # Collection operations
│   ├── embedding.py     # Embedding operations
│   ├── index.py         # Index/search operations
│   ├── client.py        # Vector service wrapper and high-level client
│   ├── exceptions.py    # Vector-specific exceptions
│   └── models/          # Vector request/response models (pydantic)
├── memory/              # Memory-specific clients and models
│   ├── __init__.py      # High-level memory client and namespace exports
│   ├── client.py        # VikingMem service client
│   ├── collection.py    # Memory collection operations
│   ├── types.py         # Type definitions for memory operations
│   └── exceptions.py    # Memory-specific exceptions

examples/
├── vector/              # Vector integration guides (pytest)
│   ├── 1_connectivity_test.py
│   ├── 2_collection_lifecycle_test.py
│   ├── 3_*_test.py     # Search and indexing examples
│   └── ...
└── memory/              # Memory usage examples
    ├── 01_init_client_and_collection.py
    ├── 02_add_session.py
    └── 03_search_memory.py
```

### Contributing

Contributions and feedback are welcome. Please ensure any new APIs match the OpenAPI specification and include accompanying example coverage.
