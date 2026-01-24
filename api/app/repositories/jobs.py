from datetime import datetime
from typing import List, Optional

from app.db.mongo import get_db


async def list_jobs() -> List[dict]:
    return await get_db().jobs.find().to_list(None)


async def get_job(job_id: str) -> Optional[dict]:
    return await get_db().jobs.find_one({"_id": job_id})


async def upsert_job(job: dict) -> None:
    job["updated_at"] = datetime.utcnow()
    await get_db().jobs.update_one({"_id": job["_id"]}, {"$set": job}, upsert=True)
