import logging
from typing import Optional
from urllib.parse import urlparse

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from app.core.config import settings

logger = logging.getLogger(__name__)

_client: Optional[QdrantClient] = None


def get_client() -> QdrantClient:
    global _client
    if _client is None:
        parsed = urlparse(settings.qdrant_url)
        host = parsed.hostname or "qdrant"
        port = parsed.port or 6333
        _client = QdrantClient(host=host, port=port)
    return _client


def ensure_collection() -> None:
    client = get_client()
    collections = client.get_collections().collections
    if any(col.name == "jobs_embeddings" for col in collections):
        return
    client.create_collection(
        collection_name="jobs_embeddings",
        vectors_config=VectorParams(size=settings.embedding_dim, distance=Distance.COSINE),
    )
    logger.info("Qdrant collection created")
