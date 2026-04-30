"""Application exception hierarchy.

All custom exceptions inherit from :class:`AppException` and carry
structured metadata used by the centralized error handlers.
"""

from __future__ import annotations

from typing import Literal


class AppException(Exception):
    """Base application exception with structured error metadata."""

    def __init__(
        self,
        error_code: str = "INTERNAL_ERROR",
        user_message: str = "An internal error occurred.",
        status_code: int = 500,
        severity: Literal["low", "medium", "high", "critical"] = "medium",
    ) -> None:
        self.error_code = error_code
        self.user_message = user_message
        self.status_code = status_code
        self.severity = severity
        super().__init__(user_message)


class AuthError(AppException):
    """Authentication or authorisation failure."""

    def __init__(
        self,
        user_message: str = "Authentication required.",
        error_code: str = "AUTH_REQUIRED",
    ) -> None:
        super().__init__(
            error_code=error_code,
            user_message=user_message,
            status_code=401,
            severity="medium",
        )


class ValidationError(AppException):
    """Request validation failure."""

    def __init__(self, user_message: str = "Validation error.") -> None:
        super().__init__(
            error_code="VALIDATION_ERROR",
            user_message=user_message,
            status_code=422,
            severity="low",
        )


class IngestionError(AppException):
    """Data ingestion failure (CSV/PDF)."""

    def __init__(self, user_message: str = "Data ingestion failed.") -> None:
        super().__init__(
            error_code="INGESTION_ERROR",
            user_message=user_message,
            status_code=400,
            severity="medium",
        )


class ToolError(AppException):
    """Tool execution failure."""

    def __init__(self, user_message: str = "Tool execution failed.") -> None:
        super().__init__(
            error_code="TOOL_ERROR",
            user_message=user_message,
            status_code=500,
            severity="high",
        )


class OrchestrationError(AppException):
    """AI model call or orchestration failure."""

    def __init__(self, user_message: str = "AI processing failed.") -> None:
        super().__init__(
            error_code="ORCHESTRATION_ERROR",
            user_message=user_message,
            status_code=500,
            severity="high",
        )
