import hashlib
import logging
import math
from typing import List

from app.core.config import settings

logger = logging.getLogger(__name__)


class Embedder:
    def __init__(self) -> None:
        self.model = None
        self.dim = settings.embedding_dim
        if settings.embed_use_sentence_transformers:
            try:
                from sentence_transformers import SentenceTransformer

                self.model = SentenceTransformer("all-MiniLM-L6-v2")
                self.dim = self.model.get_sentence_embedding_dimension()
                logger.info("Loaded sentence-transformers model")
            except Exception as exc:
                logger.warning("Sentence-transformers unavailable, fallback to hashing: %s", exc)
                self.model = None

    def embed(self, texts: List[str]) -> List[List[float]]:
        if self.model:
            vectors = self.model.encode(texts, normalize_embeddings=True).tolist()
            return vectors
        return [self._hash_embed(text) for text in texts]

    def _hash_embed(self, text: str) -> List[float]:
        vec = [0.0] * self.dim
        tokens = [token for token in text.lower().split() if token]
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
            idx = int(digest[:8], 16) % self.dim
            sign = 1.0 if int(digest[8:16], 16) % 2 == 0 else -1.0
            vec[idx] += sign
        norm = math.sqrt(sum(val * val for val in vec)) or 1.0
        return [val / norm for val in vec]


_embedder: Embedder | None = None


def get_embedder() -> Embedder:
    global _embedder
    if _embedder is None:
        _embedder = Embedder()
    return _embedder
