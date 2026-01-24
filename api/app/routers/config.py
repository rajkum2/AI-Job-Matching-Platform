from datetime import datetime

from fastapi import APIRouter, Depends

from app.core.security import require_admin
from app.models.schemas import MatchingConfigRequest
from app.repositories import audit as audit_repo
from app.repositories import config as config_repo
from app.services.matching import get_or_create_config

router = APIRouter(prefix="/config", tags=["config"], dependencies=[Depends(require_admin)])


@router.get("/matching")
async def get_matching_config():
    return await get_or_create_config()


@router.get("/matching/versions")
async def list_matching_versions():
    return await config_repo.list_configs()


@router.post("/matching")
async def create_matching_config(payload: MatchingConfigRequest):
    version = f"v{int(datetime.utcnow().timestamp())}"
    config = await config_repo.create_config(payload.weights, payload.thresholds, version)
    await audit_repo.log_event("admin", "create_matching_config", "config", version, None, config)
    return config
