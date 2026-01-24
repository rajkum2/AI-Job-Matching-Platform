import re
from typing import Dict, List

from app.services.mapping_service import get_skill_alias_map, get_title_alias_map

KNOWN_SKILLS = [
    "python",
    "fastapi",
    "django",
    "flask",
    "javascript",
    "typescript",
    "react",
    "next.js",
    "node",
    "mongodb",
    "postgresql",
    "qdrant",
    "docker",
    "kubernetes",
    "aws",
    "gcp",
    "azure",
    "ml",
    "nlp",
    "pytorch",
    "sql",
    "data pipelines",
    "airflow",
    "spark",
    "redis",
    "graphql",
]

DOMAIN_TAGS = {
    "ml": ["machine learning", "ml", "model", "nlp"],
    "backend": ["api", "backend", "microservice", "fastapi", "django", "flask"],
    "frontend": ["frontend", "react", "next.js", "ui"],
    "data": ["etl", "data pipeline", "warehouse", "spark"],
    "infra": ["kubernetes", "docker", "aws", "gcp", "azure"],
}

SENIORITY_KEYWORDS = {
    "junior": ["junior", "jr", "entry"],
    "mid": ["mid", "sde2", "ii"],
    "senior": ["senior", "sr", "iii"],
    "lead": ["lead", "principal", "staff"],
}


def _extract_skills(text: str, alias_map: Dict[str, str]) -> List[str]:
    text_lower = text.lower()
    found = set()

    for skill in KNOWN_SKILLS:
        if skill in text_lower:
            found.add(skill)

    for alias, canonical in alias_map.items():
        if alias in text_lower:
            found.add(canonical)

    normalized = set()
    for skill in found:
        normalized.add(alias_map.get(skill, skill))

    return sorted(normalized)


def _extract_domain_tags(text: str) -> List[str]:
    text_lower = text.lower()
    tags = set()
    for tag, keywords in DOMAIN_TAGS.items():
        if any(keyword in text_lower for keyword in keywords):
            tags.add(tag)
    return sorted(tags)


def _extract_seniority(text: str, title_alias: Dict[str, dict]) -> str:
    text_lower = text.lower()
    for alias, payload in title_alias.items():
        if alias in text_lower and payload.get("seniority_band"):
            return payload["seniority_band"]

    for band, keywords in SENIORITY_KEYWORDS.items():
        if any(re.search(rf"\b{re.escape(keyword)}\b", text_lower) for keyword in keywords):
            return band
    return "mid"


def _extract_title(text: str, title_alias: Dict[str, dict]) -> str:
    text_lower = text.lower()
    for alias, payload in title_alias.items():
        if alias in text_lower:
            return payload["canonical"]
    match = re.search(r"(software engineer|data scientist|ml engineer|backend engineer|frontend engineer)", text_lower)
    if match:
        return match.group(1)
    return "software engineer"


async def normalize_text(raw_text: str) -> Dict[str, object]:
    skill_alias_map = await get_skill_alias_map()
    title_alias_map = await get_title_alias_map()
    canonical_title = _extract_title(raw_text, title_alias_map)
    skills = _extract_skills(raw_text, skill_alias_map)
    seniority_band = _extract_seniority(raw_text, title_alias_map)
    domain_tags = _extract_domain_tags(raw_text)
    return {
        "canonical_title": canonical_title,
        "skills": skills,
        "seniority_band": seniority_band,
        "domain_tags": domain_tags,
        "summary": f"{canonical_title} with skills {', '.join(skills)}",
    }
