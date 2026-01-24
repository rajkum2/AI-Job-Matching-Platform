from fastapi import APIRouter, Depends

from app.core.security import require_admin
from app.models.schemas import MappingRequest
from app.repositories import audit as audit_repo
from app.repositories import mappings as mappings_repo

router = APIRouter(prefix="/mappings", tags=["mappings"], dependencies=[Depends(require_admin)])


@router.post("/skills")
async def create_skill_mapping(payload: MappingRequest):
    mapping = await mappings_repo.upsert_skill_alias(payload.alias, payload.canonical)
    await audit_repo.log_event("admin", "create_skill_alias", "mapping", mapping["_id"], None, mapping)
    return mapping


@router.get("/skills")
async def list_skill_mappings():
    return await mappings_repo.list_skill_aliases()


@router.delete("/skills/{mapping_id}")
async def delete_skill_mapping(mapping_id: str):
    await mappings_repo.delete_skill_alias(mapping_id)
    await audit_repo.log_event("admin", "delete_skill_alias", "mapping", mapping_id, None, None)
    return {"deleted": True}


@router.post("/titles")
async def create_title_mapping(payload: MappingRequest):
    mapping = await mappings_repo.upsert_title_alias(payload.alias, payload.canonical, payload.seniority_band)
    await audit_repo.log_event("admin", "create_title_alias", "mapping", mapping["_id"], None, mapping)
    return mapping


@router.get("/titles")
async def list_title_mappings():
    return await mappings_repo.list_title_aliases()


@router.delete("/titles/{mapping_id}")
async def delete_title_mapping(mapping_id: str):
    await mappings_repo.delete_title_alias(mapping_id)
    await audit_repo.log_event("admin", "delete_title_alias", "mapping", mapping_id, None, None)
    return {"deleted": True}
