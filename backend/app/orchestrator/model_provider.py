"""Model provider interface and OpenAI implementation.

Defines the :class:`ModelProvider` protocol that abstracts AI model
interactions, along with supporting data classes and a concrete
:class:`OpenAIProvider` implementation using the OpenAI chat completions API.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

import structlog
from openai import AsyncOpenAI

from app.config.settings import settings

logger = structlog.get_logger(__name__)

# Retry config for transient errors (503, 429, etc.)
_MAX_RETRIES = 3
_RETRY_DELAY_SECONDS = [2, 5, 10]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class ToolCall:
    """Represents a single tool/function call requested by the model."""

    id: str
    function_name: str
    arguments: dict[str, Any]


@dataclass
class ModelResponse:
    """Response returned by a model provider."""

    content: str | None
    tool_calls: list[ToolCall] = field(default_factory=list)
    finish_reason: str = "stop"


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class ModelProvider(Protocol):
    """Protocol that every model provider must satisfy."""

    async def chat_completion(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> ModelResponse:
        """Send messages to the model and return a response.

        Parameters
        ----------
        messages:
            List of message dicts with ``role`` and ``content`` keys.
        tools:
            Optional list of tool/function definitions in OpenAI format.
        """
        ...


# ---------------------------------------------------------------------------
# OpenAI implementation
# ---------------------------------------------------------------------------


class OpenAIProvider:
    """Model provider backed by an OpenAI-compatible chat completions API.

    Works with OpenAI, Google Gemini (via OpenAI compatibility layer),
    and other compatible providers.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self._api_key = api_key or settings.gemini_api_key or settings.openai_api_key
        self._model_name = model_name or settings.model_name

        # Determine base URL: explicit > Gemini default > OpenAI default
        resolved_base_url = base_url or settings.openai_base_url
        if not resolved_base_url and settings.model_provider == "gemini":
            resolved_base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

        client_kwargs: dict[str, Any] = {"api_key": self._api_key}
        if resolved_base_url:
            client_kwargs["base_url"] = resolved_base_url

        self._client = AsyncOpenAI(**client_kwargs)

    async def chat_completion(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> ModelResponse:
        """Call the chat completions endpoint with retry for transient errors."""
        kwargs: dict[str, Any] = {
            "model": self._model_name,
            "messages": messages,
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        logger.debug(
            "model_request",
            model=self._model_name,
            message_count=len(messages),
            tool_count=len(tools) if tools else 0,
        )

        last_error = None
        for attempt in range(_MAX_RETRIES):
            try:
                response = await self._client.chat.completions.create(**kwargs)
                break
            except Exception as exc:
                last_error = exc
                error_str = str(exc)
                # Retry on 503 (overloaded) and 429 (rate limit)
                if "503" in error_str or "429" in error_str or "UNAVAILABLE" in error_str:
                    delay = _RETRY_DELAY_SECONDS[min(attempt, len(_RETRY_DELAY_SECONDS) - 1)]
                    logger.warning(
                        "model_request_retrying",
                        attempt=attempt + 1,
                        delay=delay,
                        error=error_str[:200],
                    )
                    await asyncio.sleep(delay)
                    continue
                raise
        else:
            raise last_error  # type: ignore[misc]

        choice = response.choices[0]
        message = choice.message

        # Parse tool calls if present
        parsed_tool_calls: list[ToolCall] = []
        if message.tool_calls:
            for tc in message.tool_calls:
                try:
                    arguments = json.loads(tc.function.arguments)
                except (json.JSONDecodeError, TypeError):
                    arguments = {}
                parsed_tool_calls.append(
                    ToolCall(
                        id=tc.id,
                        function_name=tc.function.name,
                        arguments=arguments,
                    )
                )

        logger.debug(
            "openai_response",
            finish_reason=choice.finish_reason,
            has_content=message.content is not None,
            tool_call_count=len(parsed_tool_calls),
        )

        return ModelResponse(
            content=message.content,
            tool_calls=parsed_tool_calls,
            finish_reason=choice.finish_reason or "stop",
        )

    @staticmethod
    def tool_to_openai_format(tool: Any) -> dict[str, Any]:
        """Convert a :class:`~app.tools.base.Tool` to OpenAI function format.

        Parameters
        ----------
        tool:
            An object satisfying the Tool protocol (name, description,
            parameters_schema).

        Returns
        -------
        dict
            A dict in the OpenAI ``tools`` format::

                {
                    "type": "function",
                    "function": {
                        "name": "...",
                        "description": "...",
                        "parameters": { ... }
                    }
                }
        """
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters_schema,
            },
        }
