"""Tool base interface and result model for the AI Insights Assistant.

Every tool in the system implements the :class:`Tool` protocol and returns
a :class:`ToolResult` instance from its ``execute`` method.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    """Structured result returned by every tool execution."""

    data: Any = Field(default=None, description="Primary payload returned by the tool")
    metadata: dict = Field(
        default_factory=dict,
        description="Auxiliary information (row count, source file, etc.)",
    )
    error: str | None = Field(
        default=None,
        description="Human-readable error message, None on success",
    )
    execution_duration_ms: float = Field(
        default=0.0,
        description="Wall-clock execution time in milliseconds",
    )


@runtime_checkable
class Tool(Protocol):
    """Protocol that every tool must satisfy."""

    @property
    def name(self) -> str:
        """Short, unique identifier used by the orchestrator (e.g. ``sql_query``)."""
        ...

    @property
    def description(self) -> str:
        """One-line description shown to the AI model for tool selection."""
        ...

    @property
    def parameters_schema(self) -> dict:
        """JSON-Schema-style dict describing accepted parameters."""
        ...

    async def execute(self, parameters: dict) -> ToolResult:
        """Run the tool with the given *parameters* and return a result."""
        ...
