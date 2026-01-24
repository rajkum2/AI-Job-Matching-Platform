from datetime import datetime
from typing import List, Optional

from app.db.mongo import get_db


async def get_resume_by_candidate(candidate_id: str) -> Optional[dict]:
    return await get_db().resumes.find_one({"candidate_id": candidate_id})


async def list_resumes() -> List[dict]:
    return await get_db().resumes.find().to_list(None)


async def upsert_resume(resume: dict) -> None:
    resume["updated_at"] = datetime.utcnow()
    await get_db().resumes.update_one({"_id": resume["_id"]}, {"$set": resume}, upsert=True)
