import logging
from typing import Any, Dict, List, Optional, Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

logger = logging.getLogger(__name__)

_client: Optional[AsyncIOMotorClient] = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongodb_uri)
    return _client


def get_db():
    return get_client()[settings.mongo_db]


async def ensure_indexes() -> None:
    db = get_db()
    await db.matches.create_index([("candidate_id", 1), ("job_id", 1)], unique=True)
    await db.matches.create_index("status")
    await db.resumes.create_index("candidate_id")
    await db.jobs.create_index([("company", 1), ("title", 1)])
    await db.mappings_skill_aliases.create_index("alias", unique=True)
    await db.mappings_title_aliases.create_index("alias", unique=True)
    await db.audit_events.create_index("created_at")
    logger.info("Mongo indexes ensured")


def serialize_doc(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Convert MongoDB document to JSON-serializable dict by converting ObjectId to string."""
    if doc is None:
        return None
    result = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            result[key] = str(value)
        elif isinstance(value, dict):
            result[key] = serialize_doc(value)
        elif isinstance(value, list):
            result[key] = [serialize_doc(v) if isinstance(v, dict) else (str(v) if isinstance(v, ObjectId) else v) for v in value]
        else:
            result[key] = value
    return result


def serialize_docs(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert list of MongoDB documents to JSON-serializable dicts."""
    return [serialize_doc(doc) for doc in docs]
