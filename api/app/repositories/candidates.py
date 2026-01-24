from datetime import datetime
from typing import List, Optional

from app.db.mongo import get_db, serialize_doc, serialize_docs


async def list_candidates() -> List[dict]:
    docs = await get_db().candidates.find().to_list(None)
    return serialize_docs(docs)


async def get_candidate(candidate_id: str) -> Optional[dict]:
    doc = await get_db().candidates.find_one({"_id": candidate_id})
    return serialize_doc(doc)


async def upsert_candidate(candidate: dict) -> None:
    candidate.setdefault("created_at", datetime.utcnow())
    await get_db().candidates.update_one({"_id": candidate["_id"]}, {"$set": candidate}, upsert=True)
