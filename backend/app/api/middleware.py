"""Request middleware for correlation IDs and request logging."""

from __future__ import annotations

import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = structlog.get_logger(__name__)


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Assigns a UUID correlation_id to every request and logs request details."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        correlation_id = str(uuid.uuid4())
        request.state.correlation_id = correlation_id

        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        # Extract user from request state if set by auth dependency
        user = "anonymous"
        if hasattr(request.state, "user"):
            user = request.state.user

        logger.info(
            "request_completed",
            endpoint=request.url.path,
            method=request.method,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
            correlation_id=correlation_id,
            user=user,
        )

        response.headers["X-Correlation-ID"] = correlation_id
        return response
