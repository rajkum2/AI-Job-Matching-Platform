from typing import List, Tuple

from qdrant_client.http.models import PointStruct, SearchRequest

from app.db.qdrant import get_client


def upsert_job_embeddings(points: List[PointStruct]) -> None:
    client = get_client()
    client.upsert(collection_name="jobs_embeddings", points=points)


def search_jobs(vector: List[float], top_k: int) -> List[Tuple[str, float, dict]]:
    client = get_client()
    results = client.search(
        collection_name="jobs_embeddings",
        query_vector=vector,
        limit=top_k,
        with_payload=True,
    )
    return [(str(hit.id), hit.score, hit.payload or {}) for hit in results]
