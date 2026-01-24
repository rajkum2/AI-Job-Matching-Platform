from fastapi import APIRouter, Depends, HTTPException

from app.core.security import require_admin
from app.repositories import jobs as jobs_repo

router = APIRouter(prefix="/jobs", tags=["jobs"], dependencies=[Depends(require_admin)])


@router.get("")
async def list_jobs():
    return await jobs_repo.list_jobs()


@router.get("/{job_id}")
async def get_job(job_id: str):
    job = await jobs_repo.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
