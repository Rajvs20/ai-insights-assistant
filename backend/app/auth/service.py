"""JWT authentication service.

Provides token creation and validation using PyJWT.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt
import structlog

from app.config.settings import settings

logger = structlog.get_logger(__name__)


class AuthService:
    """Handles JWT token creation and validation."""

    def create_token(self, username: str) -> str:
        """Create a JWT token for the given *username*.

        The token includes ``sub`` (username) and ``exp`` (expiration) claims.
        """
        now = datetime.now(timezone.utc)
        payload = {
            "sub": username,
            "exp": now + timedelta(minutes=settings.jwt_expiration_minutes),
            "iat": now,
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        logger.info("token_created", username=username)
        return token

    def validate_token(self, token: str) -> dict:
        """Validate and decode a JWT token.

        Returns the decoded payload dict on success.
        Raises ``jwt.InvalidTokenError`` (or subclass) on failure.
        """
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
