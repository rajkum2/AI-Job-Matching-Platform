import logging
from typing import Dict, List, Tuple

from app.core.config import settings
from app.repositories import config as config_repo
from app.services.embedding import get_embedder
from app.services.qdrant_service import search_jobs

logger = logging.getLogger(__name__)


async def get_or_create_config() -> dict:
    config = await config_repo.get_latest_config()
    if config:
        return config
    weights = {
        "skill_overlap_score": 0.45,
        "title_fit_score": 0.25,
        "seniority_fit_score": 0.15,
        "domain_fit_score": 0.15,
    }
    thresholds = {"min_score": 0.2}
    return await config_repo.create_config(weights, thresholds, version="v1")


def _score_skill_overlap(candidate_skills: List[str], job_skills: List[str]) -> float:
    if not job_skills:
        return 0.0
    overlap = len(set(candidate_skills) & set(job_skills))
    return overlap / max(len(job_skills), 1)


def _score_title_fit(candidate_title: str, job_title: str) -> float:
    if candidate_title == job_title:
        return 1.0
    candidate_tokens = set(candidate_title.split())
    job_tokens = set(job_title.split())
    if not candidate_tokens or not job_tokens:
        return 0.0
    return len(candidate_tokens & job_tokens) / len(job_tokens)


def _score_seniority(candidate_band: str, job_band: str) -> float:
    if candidate_band == job_band:
        return 1.0
    bands = ["junior", "mid", "senior", "lead"]
    try:
        delta = abs(bands.index(candidate_band) - bands.index(job_band))
        return 0.7 if delta == 1 else 0.3
    except ValueError:
        return 0.0


def _score_domain(candidate_tags: List[str], job_tags: List[str]) -> float:
    if not job_tags:
        return 0.0
    overlap = len(set(candidate_tags) & set(job_tags))
    return overlap / len(job_tags)


def _build_reasons(score_breakdown: Dict[str, float]) -> List[str]:
    reasons = []
    for key, score in score_breakdown.items():
        if score >= 0.7:
            reasons.append(f"Strong {key.replace('_', ' ')}")
        elif score >= 0.4:
            reasons.append(f"Moderate {key.replace('_', ' ')}")
    if not reasons:
        reasons.append("Limited overlap, low confidence match")
    return reasons


def _weighted_score(weights: Dict[str, float], breakdown: Dict[str, float]) -> float:
    total_weight = sum(weights.values()) or 1.0
    return sum(weights.get(key, 0.0) * breakdown.get(key, 0.0) for key in breakdown) / total_weight


def candidate_summary(parsed_profile: dict) -> str:
    return " ".join(
        [
            parsed_profile.get("canonical_title", ""),
            " ".join(parsed_profile.get("skills", [])),
            " ".join(parsed_profile.get("domain_tags", [])),
        ]
    ).strip()


async def retrieve_job_candidates(parsed_profile: dict, top_k: int | None = None) -> List[Tuple[str, float, dict]]:
    top_k = top_k or settings.match_top_k
    summary = candidate_summary(parsed_profile)
    vector = get_embedder().embed([summary])[0]
    return search_jobs(vector, top_k)


async def score_match(parsed_profile: dict, job_payload: dict, weights: Dict[str, float]) -> Tuple[float, Dict[str, float], List[str]]:
    breakdown = {
        "skill_overlap_score": _score_skill_overlap(parsed_profile.get("skills", []), job_payload.get("skills", [])),
        "title_fit_score": _score_title_fit(parsed_profile.get("canonical_title", ""), job_payload.get("canonical_title", "")),
        "seniority_fit_score": _score_seniority(parsed_profile.get("seniority_band", "mid"), job_payload.get("seniority_band", "mid")),
        "domain_fit_score": _score_domain(parsed_profile.get("domain_tags", []), job_payload.get("domain_tags", [])),
    }
    final_score = _weighted_score(weights, breakdown)
    reasons = _build_reasons(breakdown)
    return final_score, breakdown, reasons
