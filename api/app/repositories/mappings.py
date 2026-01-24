from datetime import datetime
from typing import List

from app.db.mongo import get_db, serialize_doc, serialize_docs


async def list_skill_aliases() -> List[dict]:
    docs = await get_db().mappings_skill_aliases.find().to_list(None)
    return serialize_docs(docs)


async def list_title_aliases() -> List[dict]:
    docs = await get_db().mappings_title_aliases.find().to_list(None)
    return serialize_docs(docs)


async def upsert_skill_alias(alias: str, canonical: str) -> dict:
    doc = {"_id": alias, "alias": alias, "canonical": canonical, "created_at": datetime.utcnow()}
    await get_db().mappings_skill_aliases.update_one({"_id": alias}, {"$set": doc}, upsert=True)
    result = await get_db().mappings_skill_aliases.find_one({"_id": alias})
    return serialize_doc(result)


async def upsert_title_alias(alias: str, canonical: str, seniority_band: str | None) -> dict:
    doc = {"_id": alias, "alias": alias, "canonical": canonical, "seniority_band": seniority_band, "created_at": datetime.utcnow()}
    await get_db().mappings_title_aliases.update_one({"_id": alias}, {"$set": doc}, upsert=True)
    result = await get_db().mappings_title_aliases.find_one({"_id": alias})
    return serialize_doc(result)


async def delete_skill_alias(alias_id: str) -> None:
    await get_db().mappings_skill_aliases.delete_one({"_id": alias_id})


async def delete_title_alias(alias_id: str) -> None:
    await get_db().mappings_title_aliases.delete_one({"_id": alias_id})
