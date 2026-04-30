"""Authentication API routes."""

from __future__ import annotations

import structlog
from fastapi import APIRouter, HTTPException, status

from app.auth.service import AuthService
from app.models.requests import LoginRequest

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])

_auth_service = AuthService()

# Hardcoded demo credentials
_DEMO_USERNAME = "admin"
_DEMO_PASSWORD = "admin123"


@router.post("/login")
async def login(body: LoginRequest):
    """Authenticate with username/password and receive a JWT token."""
    if body.username != _DEMO_USERNAME or body.password != _DEMO_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = _auth_service.create_token(body.username)
    logger.info("user_logged_in", username=body.username)
    return {"access_token": token, "token_type": "bearer"}
