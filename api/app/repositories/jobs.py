from datetime import datetime
from typing import List, Optional

from app.db.mongo import get_db, serialize_doc, serialize_docs


async def list_jobs() -> List[dict]:
    docs = await get_db().jobs.find().to_list(None)
    return serialize_docs(docs)


async def get_job(job_id: str) -> Optional[dict]:
    doc = await get_db().jobs.find_one({"_id": job_id})
    return serialize_doc(doc)


async def upsert_job(job: dict) -> None:
    job["updated_at"] = datetime.utcnow()
    await get_db().jobs.update_one({"_id": job["_id"]}, {"$set": job}, upsert=True)
