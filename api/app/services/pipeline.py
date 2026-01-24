import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from qdrant_client.http.models import PointStruct

from app.core.config import settings
from app.repositories import audit as audit_repo
from app.db.mongo import get_db
from app.repositories import candidates as candidates_repo
from app.repositories import jobs as jobs_repo
from app.repositories import matches as matches_repo
from app.repositories import resumes as resumes_repo
from app.services.embedding import get_embedder
from app.services.matching import get_or_create_config, retrieve_job_candidates, score_match
from app.services.normalization import normalize_text
from app.services.qdrant_service import upsert_job_embeddings

logger = logging.getLogger(__name__)

SEED_DIR = Path(__file__).resolve().parents[2] / "seeds"


async def seed_data() -> Dict[str, int]:
    db = get_db()
    counts = {}
    for name in ["candidates", "resumes", "jobs"]:
        path = SEED_DIR / f"{name}.json"
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if data:
            for doc in data:
                await db[name].update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)
        counts[name] = len(data)

    await audit_repo.log_event("system", "seed", "pipeline", "seed", None, counts)
    logger.info("Seeded data: %s", counts)
    return counts


async def normalize_all() -> Dict[str, int]:
    resumes = await resumes_repo.list_resumes()
    jobs = await jobs_repo.list_jobs()
    resume_count = 0
    job_count = 0
    for resume in resumes:
        parsed = await normalize_text(resume["raw_text"])
        resume["parsed_profile"] = parsed
        resume["profile_version"] = "v1"
        await resumes_repo.upsert_resume(resume)
        resume_count += 1

    for job in jobs:
        parsed = await normalize_text(job["raw_text"])
        job["parsed_job"] = parsed
        job["job_version"] = "v1"
        await jobs_repo.upsert_job(job)
        job_count += 1

    await audit_repo.log_event("system", "normalize_all", "pipeline", "normalize", None, {"resumes": resume_count, "jobs": job_count})
    return {"resumes": resume_count, "jobs": job_count}


async def embed_jobs() -> Dict[str, int]:
    jobs = await jobs_repo.list_jobs()
    embedder = get_embedder()
    points: List[PointStruct] = []
    for job in jobs:
        parsed = job.get("parsed_job") or await normalize_text(job["raw_text"])
        job["parsed_job"] = parsed
        await jobs_repo.upsert_job(job)
        summary = parsed.get("summary", job.get("raw_text", ""))
        vector = embedder.embed([summary])[0]
        payload = {
            "job_id": job["_id"],
            "canonical_title": parsed.get("canonical_title"),
            "skills": parsed.get("skills", []),
            "seniority_band": parsed.get("seniority_band"),
            "domain_tags": parsed.get("domain_tags", []),
        }
        points.append(PointStruct(id=job["_id"], vector=vector, payload=payload))

    if points:
        upsert_job_embeddings(points)
    await audit_repo.log_event("system", "embed_jobs", "pipeline", "embed", None, {"jobs": len(points)})
    return {"jobs": len(points)}


async def match_candidate(candidate_id: str) -> Dict[str, object]:
    resume = await resumes_repo.get_resume_by_candidate(candidate_id)
    if not resume:
        return {"matches": [], "message": "Resume not found"}

    parsed_profile = resume.get("parsed_profile") or await normalize_text(resume["raw_text"])
    resume["parsed_profile"] = parsed_profile
    await resumes_repo.upsert_resume(resume)

    config = await get_or_create_config()
    weights = config["weights"]

    previous_matches = await matches_repo.list_matches_by_candidate(candidate_id)
    before_snapshot = {
        item["job_id"]: {"score": item["final_score"], "rank": idx + 1}
        for idx, item in enumerate(sorted(previous_matches, key=lambda m: m["final_score"], reverse=True))
    }

    results = await retrieve_job_candidates(parsed_profile)
    new_matches = []

    for rank, (job_id, retrieval_score, payload) in enumerate(results, start=1):
        final_score, breakdown, reasons = await score_match(parsed_profile, payload, weights)
        match_doc = {
            "_id": f"{candidate_id}:{job_id}",
            "candidate_id": candidate_id,
            "job_id": job_id,
            "final_score": float(final_score),
            "score_breakdown": breakdown,
            "reasons": reasons,
            "status": "unreviewed",
            "reject_reason_codes": [],
            "reviewer_notes": None,
            "engine_version": "v1",
            "weights_version": config["version"],
            "created_at": datetime.utcnow(),
            "retrieval_rank": rank,
            "retrieval_score": retrieval_score,
        }
        await matches_repo.upsert_match(match_doc)
        new_matches.append(match_doc)

    after_snapshot = {
        item["job_id"]: {"score": item["final_score"], "rank": idx + 1}
        for idx, item in enumerate(sorted(new_matches, key=lambda m: m["final_score"], reverse=True))
    }

    comparison = []
    for job_id, after in after_snapshot.items():
        before = before_snapshot.get(job_id)
        comparison.append(
            {
                "job_id": job_id,
                "before_rank": before["rank"] if before else None,
                "after_rank": after["rank"],
                "before_score": before["score"] if before else None,
                "after_score": after["score"],
            }
        )

    await audit_repo.log_event("system", "match_candidate", "candidate", candidate_id, None, {"matches": len(new_matches)})
    return {"matches": new_matches, "comparison": comparison}


async def match_all() -> Dict[str, int]:
    candidates = await candidates_repo.list_candidates()
    total_matches = 0
    for candidate in candidates:
        result = await match_candidate(candidate["_id"])
        total_matches += len(result.get("matches", []))
    await audit_repo.log_event("system", "match_all", "pipeline", "match", None, {"matches": total_matches})
    return {"matches": total_matches}
