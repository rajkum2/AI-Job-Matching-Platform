import asyncio
import logging
from urllib.parse import urlparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import configure_logging
from app.core.config import settings
from app.db.mongo import ensure_indexes
from app.db.qdrant import ensure_collection
from app.routers import admin, audit, auth, candidates, config, jobs, mappings, matches

logger = logging.getLogger(__name__)

app = FastAPI(title="JobMatch MVP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    configure_logging()
    await _validate_env()
    await _wait_for_dependencies()
    await ensure_indexes()
    ensure_collection()


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(candidates.router)
app.include_router(jobs.router)
app.include_router(matches.router)
app.include_router(mappings.router)
app.include_router(config.router)
app.include_router(audit.router)


async def _validate_env() -> None:
    if not settings.mongodb_uri:
        raise RuntimeError("MONGODB_URI is required")
    if not settings.qdrant_url:
        raise RuntimeError("QDRANT_URL is required")
    if not settings.admin_password:
        raise RuntimeError("ADMIN_PASSWORD is required")
    if not settings.admin_token_secret:
        raise RuntimeError("ADMIN_TOKEN_SECRET is required")


async def _wait_for_dependencies() -> None:
    from motor.motor_asyncio import AsyncIOMotorClient
    from qdrant_client import QdrantClient

    mongo_client = AsyncIOMotorClient(settings.mongodb_uri)
    qdrant_parsed = urlparse(settings.qdrant_url)
    qdrant_client = QdrantClient(host=qdrant_parsed.hostname or "qdrant", port=qdrant_parsed.port or 6333)

    for attempt in range(10):
        try:
            await mongo_client.admin.command("ping")
            qdrant_client.get_collections()
            logger.info("Dependencies ready")
            return
        except Exception as exc:
            wait = 2 + attempt
            logger.warning("Waiting for dependencies: %s", exc)
            await asyncio.sleep(wait)
    raise RuntimeError("Dependencies are not ready after retries")
