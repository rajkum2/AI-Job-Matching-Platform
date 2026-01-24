from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Candidate(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: Optional[str] = None
    created_at: datetime


class Resume(BaseModel):
    id: str = Field(alias="_id")
    candidate_id: str
    raw_text: str
    parsed_profile: Optional[Dict[str, Any]] = None
    profile_version: Optional[str] = None
    updated_at: datetime


class Job(BaseModel):
    id: str = Field(alias="_id")
    company: str
    title: str
    raw_text: str
    parsed_job: Optional[Dict[str, Any]] = None
    job_version: Optional[str] = None
    updated_at: datetime


class Match(BaseModel):
    id: str = Field(alias="_id")
    candidate_id: str
    job_id: str
    final_score: float
    score_breakdown: Dict[str, float]
    reasons: List[str]
    status: str
    reject_reason_codes: List[str] = []
    reviewer_notes: Optional[str] = None
    engine_version: str
    weights_version: str
    created_at: datetime


class MappingAlias(BaseModel):
    id: str = Field(alias="_id")
    alias: str
    canonical: str
    seniority_band: Optional[str] = None
    created_at: datetime


class MatchingConfig(BaseModel):
    id: str = Field(alias="_id")
    weights: Dict[str, float]
    thresholds: Dict[str, float]
    version: str
    updated_at: datetime


class AuditEvent(BaseModel):
    id: str = Field(alias="_id")
    actor: str
    action: str
    entity_type: str
    entity_id: str
    before: Optional[Dict[str, Any]] = None
    after: Optional[Dict[str, Any]] = None
    created_at: datetime


class LoginRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    token: str
    expires_in: int


class ApproveRequest(BaseModel):
    reviewer_notes: Optional[str] = None


class RejectRequest(BaseModel):
    reject_reason_codes: List[str]
    reviewer_notes: Optional[str] = None


class MappingRequest(BaseModel):
    alias: str
    canonical: str
    seniority_band: Optional[str] = None


class MatchingConfigRequest(BaseModel):
    weights: Dict[str, float]
    thresholds: Dict[str, float]
