from datetime import datetime
from typing import Optional

from app.db.mongo import get_db, serialize_doc, serialize_docs


async def get_latest_config() -> Optional[dict]:
    doc = await get_db().matching_config.find_one(sort=[("updated_at", -1)])
    return serialize_doc(doc)


async def create_config(weights: dict, thresholds: dict, version: str) -> dict:
    doc = {
        "_id": version,
        "weights": weights,
        "thresholds": thresholds,
        "version": version,
        "updated_at": datetime.utcnow(),
    }
    await get_db().matching_config.insert_one(doc)
    return serialize_doc(doc)


async def list_configs() -> list[dict]:
    docs = await get_db().matching_config.find().sort("updated_at", -1).to_list(50)
    return serialize_docs(docs)
