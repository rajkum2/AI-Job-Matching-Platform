from datetime import datetime
from typing import List, Optional

from app.db.mongo import get_db


async def list_candidates() -> List[dict]:
    return await get_db().candidates.find().to_list(None)


async def get_candidate(candidate_id: str) -> Optional[dict]:
    return await get_db().candidates.find_one({"_id": candidate_id})


async def upsert_candidate(candidate: dict) -> None:
    candidate.setdefault("created_at", datetime.utcnow())
    await get_db().candidates.update_one({"_id": candidate["_id"]}, {"$set": candidate}, upsert=True)
