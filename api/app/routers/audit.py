from fastapi import APIRouter, Depends

from app.core.security import require_admin
from app.repositories import audit as audit_repo

router = APIRouter(prefix="/audit", tags=["audit"], dependencies=[Depends(require_admin)])


@router.get("")
async def list_audit_events():
    return await audit_repo.list_events()
