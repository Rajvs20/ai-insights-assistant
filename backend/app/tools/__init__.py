"""Tool layer package.

Provides the :data:`tool_registry` dict for dynamic tool lookup by name,
and re-exports the base interface types.
"""

from __future__ import annotations

from app.tools.base import Tool, ToolResult

# Registry mapping tool name → tool instance.
# Populated at application startup (e.g. in main.py or orchestrator init).
tool_registry: dict[str, Tool] = {}

__all__ = ["Tool", "ToolResult", "tool_registry"]
