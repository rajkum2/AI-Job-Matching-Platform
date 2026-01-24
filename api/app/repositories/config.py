from datetime import datetime
from typing import Optional

from app.db.mongo import get_db


async def get_latest_config() -> Optional[dict]:
    return await get_db().matching_config.find_one(sort=[("updated_at", -1)])


async def create_config(weights: dict, thresholds: dict, version: str) -> dict:
    doc = {
        "_id": version,
        "weights": weights,
        "thresholds": thresholds,
        "version": version,
        "updated_at": datetime.utcnow(),
    }
    await get_db().matching_config.insert_one(doc)
    return doc


async def list_configs() -> list[dict]:
    return await get_db().matching_config.find().sort("updated_at", -1).to_list(50)
