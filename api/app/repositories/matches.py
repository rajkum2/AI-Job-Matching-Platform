from datetime import datetime
from typing import List, Optional

from app.db.mongo import get_db


async def list_matches(status: Optional[str] = None) -> List[dict]:
    query = {"status": status} if status else {}
    return await get_db().matches.find(query).to_list(None)


async def get_match(match_id: str) -> Optional[dict]:
    return await get_db().matches.find_one({"_id": match_id})


async def upsert_match(match: dict) -> None:
    match.setdefault("created_at", datetime.utcnow())
    await get_db().matches.update_one({"_id": match["_id"]}, {"$set": match}, upsert=True)


async def list_matches_by_candidate(candidate_id: str) -> List[dict]:
    return await get_db().matches.find({"candidate_id": candidate_id}).to_list(None)


async def update_match_status(match_id: str, status: str, reject_reason_codes: List[str], reviewer_notes: Optional[str]) -> dict:
    await get_db().matches.update_one(
        {"_id": match_id},
        {"$set": {"status": status, "reject_reason_codes": reject_reason_codes, "reviewer_notes": reviewer_notes}},
    )
    return await get_match(match_id)
