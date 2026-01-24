from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.core.security import issue_token
from app.models.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest):
    if payload.password != settings.admin_password:
        raise HTTPException(status_code=401, detail="Invalid password")
    token = issue_token()
    return LoginResponse(token=token, expires_in=3600)
