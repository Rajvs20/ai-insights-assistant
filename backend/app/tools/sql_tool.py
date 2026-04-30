"""SQL Query Tool – executes SQL against the SQLite database.

The AI model generates the SQL string and passes it as the ``query``
parameter.  The tool executes it via SQLAlchemy :func:`sqlalchemy.text`,
enforces the configured row limit, and returns structured results.
"""

from __future__ import annotations

import time

import structlog
from sqlalchemy import text

from app.config.settings import settings
from app.models.database import get_session
from app.tools.base import ToolResult

logger = structlog.get_logger(__name__)


class SQLQueryTool:
    """Tool that runs a raw SQL query against the application database."""

    @property
    def name(self) -> str:
        return "sql_query"

    @property
    def description(self) -> str:
        return (
            "Execute a SQL query against the entertainment analytics database "
            "and return the result set as a list of row dicts."
        )

    @property
    def parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL query to execute.",
                },
            },
            "required": ["query"],
        }

    async def execute(self, parameters: dict) -> ToolResult:
        """Execute the SQL *query* and return rows as list-of-dicts."""
        query_str: str = parameters.get("query", "").strip()
        if not query_str:
            return ToolResult(
                data=None,
                error="No query provided.",
                execution_duration_ms=0.0,
            )

        session = get_session()
        start = time.perf_counter()
        try:
            result_proxy = session.execute(text(query_str))
            columns = list(result_proxy.keys())
            rows = [dict(zip(columns, row)) for row in result_proxy.fetchall()]

            # Enforce row limit
            truncated = len(rows) > settings.sql_row_limit
            rows = rows[: settings.sql_row_limit]

            elapsed_ms = (time.perf_counter() - start) * 1000

            logger.info(
                "sql_query_executed",
                query=query_str,
                duration_ms=round(elapsed_ms, 2),
                row_count=len(rows),
                truncated=truncated,
            )

            metadata: dict = {
                "row_count": len(rows),
                "columns": columns,
                "truncated": truncated,
            }

            return ToolResult(
                data=rows,
                metadata=metadata,
                execution_duration_ms=round(elapsed_ms, 2),
            )

        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.error(
                "sql_query_failed",
                query=query_str,
                duration_ms=round(elapsed_ms, 2),
                error=str(exc),
            )
            return ToolResult(
                data=None,
                error="Query execution failed. Please check the query syntax and try again.",
                execution_duration_ms=round(elapsed_ms, 2),
            )
        finally:
            session.close()
