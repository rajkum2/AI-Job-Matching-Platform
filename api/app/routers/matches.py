from fastapi import APIRouter, Depends, HTTPException

from app.core.security import require_admin
from app.models.schemas import ApproveRequest, RejectRequest
from app.repositories import audit as audit_repo
from app.repositories import matches as matches_repo

router = APIRouter(prefix="/matches", tags=["matches"], dependencies=[Depends(require_admin)])


@router.get("")
async def list_matches(status: str | None = None):
    return await matches_repo.list_matches(status)


@router.get("/{match_id}")
async def get_match(match_id: str):
    match = await matches_repo.get_match(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.post("/{match_id}/approve")
async def approve_match(match_id: str, payload: ApproveRequest):
    before = await matches_repo.get_match(match_id)
    if not before:
        raise HTTPException(status_code=404, detail="Match not found")
    updated = await matches_repo.update_match_status(match_id, "approved", [], payload.reviewer_notes)
    await audit_repo.log_event("admin", "approve_match", "match", match_id, before, updated)
    return updated


@router.post("/{match_id}/reject")
async def reject_match(match_id: str, payload: RejectRequest):
    before = await matches_repo.get_match(match_id)
    if not before:
        raise HTTPException(status_code=404, detail="Match not found")
    updated = await matches_repo.update_match_status(match_id, "rejected", payload.reject_reason_codes, payload.reviewer_notes)
    await audit_repo.log_event("admin", "reject_match", "match", match_id, before, updated)
    return updated
