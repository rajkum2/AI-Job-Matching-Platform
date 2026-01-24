from typing import Dict

from app.repositories import mappings as mappings_repo


async def get_skill_alias_map() -> Dict[str, str]:
    aliases = await mappings_repo.list_skill_aliases()
    return {item["alias"].lower(): item["canonical"].lower() for item in aliases}


async def get_title_alias_map() -> Dict[str, dict]:
    aliases = await mappings_repo.list_title_aliases()
    return {
        item["alias"].lower(): {
            "canonical": item["canonical"].lower(),
            "seniority_band": item.get("seniority_band"),
        }
        for item in aliases
    }
