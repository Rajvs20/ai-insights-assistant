"""Pydantic request models for API endpoints."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from app.config.settings import settings


class LoginRequest(BaseModel):
    """Credentials for the login endpoint."""

    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=200)


class TimePeriod(BaseModel):
    """Date range filter."""

    start_date: date
    end_date: date


class Filters(BaseModel):
    """Optional filters applied to a chat question."""

    time_period: TimePeriod | None = None
    genres: list[str] | None = None
    regions: list[str] | None = None


class ChatRequest(BaseModel):
    """Payload for the chat endpoint."""

    question: str = Field(..., min_length=1, max_length=settings.max_question_length)
    filters: Filters | None = None
    session_id: str | None = None
