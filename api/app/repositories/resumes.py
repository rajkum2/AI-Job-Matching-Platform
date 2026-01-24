from datetime import datetime
from typing import List, Optional

from app.db.mongo import get_db, serialize_doc, serialize_docs


async def get_resume_by_candidate(candidate_id: str) -> Optional[dict]:
    doc = await get_db().resumes.find_one({"candidate_id": candidate_id})
    return serialize_doc(doc)


async def list_resumes() -> List[dict]:
    docs = await get_db().resumes.find().to_list(None)
    return serialize_docs(docs)


async def upsert_resume(resume: dict) -> None:
    resume["updated_at"] = datetime.utcnow()
    await get_db().resumes.update_one({"_id": resume["_id"]}, {"$set": resume}, upsert=True)
