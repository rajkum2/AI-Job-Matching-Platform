from fastapi import APIRouter, Depends, HTTPException

from app.core.security import require_admin
from app.repositories import candidates as candidates_repo
from app.repositories import resumes as resumes_repo

router = APIRouter(prefix="/candidates", tags=["candidates"], dependencies=[Depends(require_admin)])


@router.get("")
async def list_candidates():
    return await candidates_repo.list_candidates()


@router.get("/{candidate_id}")
async def get_candidate(candidate_id: str):
    candidate = await candidates_repo.get_candidate(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    resume = await resumes_repo.get_resume_by_candidate(candidate_id)
    return {"candidate": candidate, "resume": resume}
