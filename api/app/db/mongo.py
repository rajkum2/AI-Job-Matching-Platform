import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

logger = logging.getLogger(__name__)

_client: Optional[AsyncIOMotorClient] = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongo_uri)
    return _client


def get_db():
    return get_client()[settings.mongo_db]


async def ensure_indexes() -> None:
    db = get_db()
    await db.matches.create_index([("candidate_id", 1), ("job_id", 1), ("status", 1)])
    await db.resumes.create_index("candidate_id")
    await db.jobs.create_index([("company", 1), ("title", 1)])
    await db.mappings_skill_aliases.create_index("alias", unique=True)
    await db.mappings_title_aliases.create_index("alias", unique=True)
    await db.audit_events.create_index("created_at")
    logger.info("Mongo indexes ensured")
