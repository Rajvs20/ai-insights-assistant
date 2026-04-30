"""Centralized FastAPI exception handlers."""

from __future__ import annotations

import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.models.errors import AppException
from app.models.responses import ErrorResponse

logger = structlog.get_logger(__name__)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle :class:`AppException` and return a structured error response."""
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    logger.error(
        "application_error",
        error_code=exc.error_code,
        correlation_id=correlation_id,
        severity=exc.severity,
        status_code=exc.status_code,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error_code=exc.error_code,
            message=exc.user_message,
            correlation_id=correlation_id,
        ).model_dump(),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions — return 500 with no internal details."""
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    logger.critical(
        "unhandled_exception",
        correlation_id=correlation_id,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_code="INTERNAL_ERROR",
            message="An internal error occurred. Please try again later.",
            correlation_id=correlation_id,
        ).model_dump(),
    )


def register_error_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI *app*."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
