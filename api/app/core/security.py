import hashlib
import time
from typing import Dict

from fastapi import Header, HTTPException

from app.core.config import settings

_tokens: Dict[str, float] = {}


def issue_token() -> str:
    now = int(time.time())
    raw = f"{settings.admin_password}:{settings.admin_token_secret}:{now}"
    token = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    _tokens[token] = now
    return token


def verify_token(token: str) -> bool:
    return token in _tokens


def require_admin(authorization: str | None = Header(default=None)) -> None:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ", 1)[1].strip()
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
