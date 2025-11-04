# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import pytest

from vikingdb import IAM, RequestOptions
from vikingdb.vector import (
    AggRequest,
    CollectionClient,
    EmbeddingClient,
    EmbeddingModelOpt,
    EmbeddingRequest,
    IndexClient,
    SearchByKeywordsRequest,
    SearchByMultiModalRequest,
    VikingDB,
)

# Pinned dataset configuration for the public guide walkthroughs.
DEFAULT_REGION = "ap-southeast-1"
DEFAULT_HOST = "api-vikingdb.vikingdb.ap-southeast-1.volces.com"
DEFAULT_ENDPOINT = f"https://{DEFAULT_HOST}"
EMBEDDING_MODEL_NAME = "bge-m3"  # dense embedding model (dim=1024) used by the guides
# --- require embedding ---------------------------------------------
TEXT_COLLECTION = "text"
TEXT_INDEX = "text_index"
# --- vectorized ----------------------------------------------------
VECTOR_COLLECTION = "vector"
VECTOR_INDEX = "vector_index"


def _load_dot_env() -> None:
    env_path = Path(".env")
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        key = key.strip()
        value = value.strip()
        os.environ.setdefault(key, value)


def require_env_vars(*names: str) -> Dict[str, str]:
    """
    Ensure the requested environment variables are present before running a snippet.
    Mirrors the Go example behaviour by skipping when configuration is missing.
    """
    _load_dot_env()
    missing = [name for name in names if not os.getenv(name)]
    if missing:
        pytest.skip(f"missing required environment variables: {', '.join(missing)}")
    return {name: os.environ[name] for name in names}


@dataclass
class EnvConfig:
    endpoint: str
    region: str
    access_key: str
    secret_key: str
    collection: str
    index: str
    project_name: Optional[str] = None
    resource_id: Optional[str] = None


@dataclass
class Clients:
    collection: CollectionClient
    index: IndexClient
    embedding: EmbeddingClient


def load_config(*, collection: str = TEXT_COLLECTION, index: str = TEXT_INDEX) -> EnvConfig:
    """
    Expect the environment (or .env) to expose only AK/SK; collection/index/region/host
    are pinned in-code so the guides target the documented datasets.

    Required:
        VIKINGDB_AK=...
        VIKINGDB_SK=...

    Override ``collection``/``index`` when a guide needs a different dataset
    (for example, the vector walkthrough points to the "vector" collection and
    "vector_index").
    """
    _load_dot_env()

    access_key = os.getenv("VIKINGDB_AK")
    secret_key = os.getenv("VIKINGDB_SK")
    if not access_key or not secret_key:
        pytest.skip("Missing required environment variables: VIKINGDB_AK and VIKINGDB_SK")

    project = os.getenv("VIKINGDB_PROJECT") or None
    resource_id = os.getenv("VIKINGDB_RESOURCE_ID") or None

    host = os.getenv("VIKINGDB_HOST", DEFAULT_HOST)
    endpoint = os.getenv("VIKINGDB_ENDPOINT") or f"https://{host}"
    region = os.getenv("VIKINGDB_REGION", DEFAULT_REGION)

    return EnvConfig(
        endpoint=endpoint,
        region=region,
        access_key=access_key,
        secret_key=secret_key,
        collection=collection,
        index=index,
        project_name=project,
        resource_id=resource_id,
    )


def build_clients(config: EnvConfig) -> Clients:
    client = VikingDB(
        endpoint=config.endpoint,
        region=config.region,
        timeout=30.0,
        user_agent="vikingdb-python-sdk-guide",
        auth=IAM(config.access_key, config.secret_key),
    )

    collection_client = client.collection(
        collection_name=config.collection,
        project_name=config.project_name,
        resource_id=config.resource_id,
    )
    index_client = client.index(
        collection_name=config.collection,
        index_name=config.index,
        project_name=config.project_name,
        resource_id=config.resource_id,
    )
    embedding_client = client.embedding()
    return Clients(collection_client, index_client, embedding_client)


def embed_dense_vectors(
    embedding_client: EmbeddingClient,
    texts: Sequence[str],
    *,
    request_options: Optional[RequestOptions] = None,
) -> List[List[float]]:
    """Return dense vectors for the supplied texts using the default guide model."""
    request = EmbeddingRequest(
        data=[{"text": text} for text in texts],
        dense_model=EmbeddingModelOpt(name=EMBEDDING_MODEL_NAME),
    )
    response = embedding_client.embedding(request, request_options=request_options)
    if not response.result or not response.result.data:
        raise AssertionError("embedding response should contain data")
    vectors: List[List[float]] = []
    for idx, item in enumerate(response.result.data):
        if not item.dense:
            raise AssertionError(f"embedding response missing dense vector at index {idx}")
        vectors.append(list(item.dense))
    if len(vectors) != len(texts):
        raise AssertionError("embedding response count does not match request payload")
    return vectors


@dataclass
class StoryChapter:
    key: str
    title: str
    paragraph: int
    score: float
    text: str
    chapter_id: Optional[Any] = None


def build_story_chapters(session_tag: str, base_paragraph: int) -> List[StoryChapter]:
    return [
        StoryChapter(
            key="orientation",
            title=f"Atlas Orientation · {session_tag}",
            paragraph=base_paragraph,
            score=72.5,
            text=f"{session_tag} — Orientation covers connectivity checks and environment hygiene before diving into search.",
        ),
        StoryChapter(
            key="retrieval-lab",
            title=f"Atlas Retrieval Lab · {session_tag}",
            paragraph=base_paragraph + 1,
            score=88.4,
            text=f"{session_tag} — Retrieval lab explores multi-modal prompts and scalar filters to focus recommendations.",
        ),
        StoryChapter(
            key="signal-tuning",
            title=f"Atlas Signal Tuning · {session_tag}",
            paragraph=base_paragraph + 2,
            score=93.1,
            text=f"{session_tag} — Signal tuning stresses analytics, aggregations, and reranking to refine the journey.",
        ),
    ]


def chapters_to_upsert(chapters: Iterable[StoryChapter]) -> List[Dict[str, Any]]:
    payload = []
    for chapter in chapters:
        payload.append(
            {
                "title": chapter.title,
                "paragraph": chapter.paragraph,
                "score": chapter.score,
                "text": chapter.text,
            }
        )
    return payload


def assign_chapter_ids_via_search(
    index_client: IndexClient,
    chapters: Sequence[StoryChapter],
    *,
    output_fields: Sequence[str],
    request_options: Optional[RequestOptions] = None,
) -> None:
    for chapter in chapters:
        hit, request_id = search_chapter_by_narrative(
            index_client,
            chapter.text,
            output_fields=output_fields,
            request_options=request_options,
        )
        chapter.chapter_id = hit.id
        print(
            f"SearchByMultiModal request_id={request_id} chapter_key={chapter.key} "
            f"id={chapter.chapter_id} title={hit.fields.get('title')!r} score={hit.fields.get('score')}"
        )


def search_chapter_by_narrative(
    index_client: IndexClient,
    query_text: str,
    *,
    output_fields: Sequence[str],
    request_options: Optional[RequestOptions] = None,
    max_attempts: int = 10,
    sleep_seconds: float = 0.5,
):
    limit = 3
    search_request = SearchByMultiModalRequest(
        text=query_text,
        need_instruction=False,
        output_fields=list(output_fields),
        limit=limit,
    )

    last_error: Optional[Exception] = None
    for attempt in range(max_attempts):
        try:
            response = index_client.search_by_multi_modal(search_request, request_options=request_options)
        except Exception as exc:  # pragma: no cover - exercised at runtime
            last_error = exc
            time.sleep(sleep_seconds)
            continue

        if response.result and response.result.data:
            return response.result.data[0], response.request_id

        last_error = None
        time.sleep(sleep_seconds)

    raise AssertionError(f"SearchByMultiModal failed to return results for query {query_text!r}: {last_error}")


def session_paragraph_bounds(base: int, count: int) -> Dict[str, Any]:
    return {"op": "range", "field": "paragraph", "gte": base, "lt": base + count}


def score_at_least_filter(min_score: float) -> Dict[str, Any]:
    return {"op": "range", "field": "score", "gt": min_score}


def bool_and_filters(filters: Sequence[Optional[Mapping[str, Any]]]) -> Optional[Dict[str, Any]]:
    usable = [f for f in filters if f]
    if not usable:
        return None
    if len(usable) == 1:
        return dict(usable[0])
    return {"op": "and", "conds": list(usable)}


def new_session_tag(prefix: str) -> str:
    return f"{prefix}-{int(time.time() * 1e9)}-{random.randint(0, 1_000)}"


def build_request_options(session_tag: str) -> RequestOptions:
    options = RequestOptions()
    options.request_id = session_tag
    return options


def cleanup_chapters(
    collection_client: CollectionClient,
    chapters: Sequence[StoryChapter],
    *,
    request_options: Optional[RequestOptions] = None,
) -> None:
    ids = [chapter.chapter_id for chapter in chapters if chapter.chapter_id is not None]
    if not ids:
        return
    collection_client.delete({"ids": ids}, request_options=request_options)


def assert_keyword_hit_titles(
    search_response,
    *,
    expected_keyword: str,
    session_tag: str,
) -> Tuple[List[str], str]:
    """
    Convenience assertion mirroring the Go guide: ensure the response contains hits
    and titles remain scoped to the session_tag.
    """
    if not search_response.result or not search_response.result.data:
        raise AssertionError("keywords search should return results")

    titles = []
    for item in search_response.result.data:
        title = item.fields.get("title")
        if title is None:
            raise AssertionError("keywords search result missing title")
        titles.append(title)
        if session_tag not in title:
            raise AssertionError(f"keywords search should remain scoped to session tag {session_tag!r}")
        # search_by_keywords only affects ranking, so exact keyword presence is best-effort
    return titles, search_response.request_id


__all__ = [
    "AggRequest",
    "Clients",
    "EnvConfig",
    "SearchByKeywordsRequest",
    "TEXT_COLLECTION",
    "TEXT_INDEX",
    "VECTOR_COLLECTION",
    "VECTOR_INDEX",
    "assign_chapter_ids_via_search",
    "build_clients",
    "build_request_options",
    "build_story_chapters",
    "chapters_to_upsert",
    "cleanup_chapters",
    "embed_dense_vectors",
    "load_config",
    "new_session_tag",
    "require_env_vars",
    "score_at_least_filter",
    "session_paragraph_bounds",
    "StoryChapter",
    "bool_and_filters",
    "assert_keyword_hit_titles",
]
