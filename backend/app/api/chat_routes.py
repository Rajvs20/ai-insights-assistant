"""Chat API routes."""

from __future__ import annotations

import structlog
from fastapi import APIRouter, Depends, Request

from app.auth.dependencies import get_current_user
from app.models.requests import ChatRequest
from app.models.responses import ChatResponse
from app.utils.sanitize import sanitize_input

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(body: ChatRequest, request: Request, user: dict = Depends(get_current_user)):
    """Submit a question to the AI assistant."""
    orchestrator = request.app.state.orchestrator

    # Sanitize the question text
    question = sanitize_input(body.question)

    # Build filters dict if provided
    filters_dict = None
    if body.filters:
        filters_dict = body.filters.model_dump(exclude_none=True)

    response = await orchestrator.process_question(
        question=question,
        filters=filters_dict,
        session_id=body.session_id,
    )
    return response


@router.get("/history/{session_id}")
async def chat_history(session_id: str, request: Request, user: dict = Depends(get_current_user)):
    """Return the conversation history for a session."""
    orchestrator = request.app.state.orchestrator
    messages = orchestrator._sessions.get(session_id, [])

    # Return only user and assistant messages (exclude system and tool messages)
    history = [
        {"role": msg["role"], "content": msg.get("content", "")}
        for msg in messages
        if msg.get("role") in ("user", "assistant")
    ]
    return {"session_id": session_id, "messages": history}
