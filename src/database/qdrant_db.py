from pathlib import Path

from qdrant_client import QdrantClient, models


# Project directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Local database storage
QDRANT_PATH = PROJECT_ROOT / "data" / "qdrant"

# Collection configuration
COLLECTION_NAME = "hybrid_documents"
VECTOR_SIZE = 384


def get_qdrant_client():
    """Connect to persistent local Qdrant storage."""

    QDRANT_PATH.mkdir(parents=True, exist_ok=True)

    return QdrantClient(path=str(QDRANT_PATH))


def ensure_collection(client):
    """Create the collection if it does not exist."""

    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE,
            ),
        )

    return COLLECTION_NAME