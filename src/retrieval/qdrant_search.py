import hashlib
import re
import uuid

from types import SimpleNamespace

from qdrant_client import models
from llama_index.core.schema import TextNode
from llama_index.retrievers.bm25 import BM25Retriever

from src.database.qdrant_db import (
    get_qdrant_client,
    ensure_collection,
    COLLECTION_NAME,
    VECTOR_SIZE,
)


def make_vector(text):
    vector = [0.0] * VECTOR_SIZE

    for word in re.findall(r"\w+", text.lower()):
        digest = hashlib.sha256(word.encode()).digest()
        index = int.from_bytes(digest[:4], "big") % VECTOR_SIZE
        vector[index] += 1.0

    magnitude = sum(value * value for value in vector) ** 0.5

    if magnitude:
        vector = [value / magnitude for value in vector]

    return vector


def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))

        if end == len(words):
            break

        start = end - overlap

    return chunks


def index_pdf(pages, file_name):
    client = get_qdrant_client()
    ensure_collection(client)

    points = []

    for page in pages:
        page_number = page.get(
            "page",
            page.get("page_number")
        )

        for chunk in chunk_text(page["text"]):
            points.append(
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=make_vector(chunk),
                    payload={
                        "file_name": file_name,
                        "page": page_number,
                        "text": chunk,
                    },
                )
            )

    if points:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )

    return len(points)


def search_pdf(query, limit=5):
    client = get_qdrant_client()
    ensure_collection(client)

    # Qdrant vector retrieval
    vector_results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=make_vector(query),
        limit=limit,
        with_payload=True,
    ).points

    # Load indexed documents for BM25
    records, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True,
        with_vectors=False,
    )

    nodes = [
        TextNode(
            id_=str(record.id),
            text=record.payload.get("text", ""),
            metadata={
                "page": record.payload.get("page"),
                "file_name": record.payload.get("file_name"),
            },
        )
        for record in records
        if record.payload and record.payload.get("text")
    ]

    if not nodes:
        return vector_results

    # BM25 keyword retrieval
    bm25 = BM25Retriever.from_defaults(
        nodes=nodes,
        similarity_top_k=limit,
    )

    keyword_results = bm25.retrieve(query)

    # Reciprocal Rank Fusion
    scores = {}
    result_map = {}

    for rank, point in enumerate(vector_results, start=1):
        key = str(point.id)
        scores[key] = scores.get(key, 0) + 1 / (60 + rank)
        result_map[key] = point

    for rank, item in enumerate(keyword_results, start=1):
        key = item.node.node_id
        scores[key] = scores.get(key, 0) + 1 / (60 + rank)

        if key not in result_map:
            result_map[key] = SimpleNamespace(
                id=key,
                payload={
                    "text": item.node.text,
                    "page": item.node.metadata.get("page"),
                    "file_name": item.node.metadata.get("file_name"),
                },
            )

    ranked = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        SimpleNamespace(
            id=key,
            payload=result_map[key].payload,
            score=score,
        )
        for key, score in ranked[:limit]
    ]