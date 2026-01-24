from fastapi import APIRouter, Depends

from app.core.security import require_admin
from app.services import pipeline

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.post("/seed")
async def seed():
    return await pipeline.seed_data()


@router.post("/normalize/all")
async def normalize_all():
    return await pipeline.normalize_all()


@router.post("/embed/jobs")
async def embed_jobs():
    return await pipeline.embed_jobs()


@router.post("/match/all")
async def match_all():
    return await pipeline.match_all()


@router.post("/match/candidate/{candidate_id}")
async def match_candidate(candidate_id: str):
    return await pipeline.match_candidate(candidate_id)
