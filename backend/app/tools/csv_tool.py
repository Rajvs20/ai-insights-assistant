"""CSV Query Tool – loads and queries registered CSV files via pandas.

Supports filtering by column values, sorting, and aggregation operations
(sum, average, count, min, max).  Validates that the requested file is
registered in the ``csv_registry`` table before processing.
"""

from __future__ import annotations

import time

import pandas as pd
import structlog

from app.config.settings import settings
from app.models.database import get_session
from app.models.tables import CSVRegistry
from app.tools.base import ToolResult

logger = structlog.get_logger(__name__)

# Allowed aggregation operations
_VALID_AGGREGATIONS = {"sum", "average", "count", "min", "max"}


class CSVQueryTool:
    """Tool that queries registered CSV files using pandas."""

    @property
    def name(self) -> str:
        return "csv_query"

    @property
    def description(self) -> str:
        return (
            "Query a registered CSV file with optional filtering, sorting, "
            "and aggregation. Returns matching rows as a list of dicts."
        )

    @property
    def parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name of the registered CSV file to query.",
                },
                "filters": {
                    "type": "object",
                    "description": (
                        "Column-value pairs to filter rows. "
                        "Each key is a column name and the value is the "
                        "required cell value."
                    ),
                },
                "sort_by": {
                    "type": "string",
                    "description": "Column name to sort results by.",
                },
                "sort_order": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "description": "Sort direction. Defaults to 'asc'.",
                },
                "aggregation": {
                    "type": "object",
                    "description": (
                        "Aggregation to apply. Must contain 'operation' "
                        "(sum | average | count | min | max) and 'column'."
                    ),
                    "properties": {
                        "operation": {"type": "string"},
                        "column": {"type": "string"},
                    },
                },
            },
            "required": ["filename"],
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _lookup_registry(filename: str) -> CSVRegistry | None:
        """Return the registry entry for *filename*, or ``None``."""
        session = get_session()
        try:
            entry = (
                session.query(CSVRegistry)
                .filter(CSVRegistry.filename == filename)
                .first()
            )
            # Detach from session so we can use it after close
            if entry is not None:
                session.expunge(entry)
            return entry
        finally:
            session.close()

    # ------------------------------------------------------------------
    # Execute
    # ------------------------------------------------------------------

    async def execute(self, parameters: dict) -> ToolResult:
        """Load, filter, sort, and/or aggregate a registered CSV file."""
        filename: str = parameters.get("filename", "").strip()
        if not filename:
            return ToolResult(
                data=None,
                error="No filename provided.",
                execution_duration_ms=0.0,
            )

        start = time.perf_counter()

        # 1. Validate registration
        registry_entry = self._lookup_registry(filename)
        if registry_entry is None:
            elapsed_ms = (time.perf_counter() - start) * 1000
            return ToolResult(
                data=None,
                error=f"CSV file '{filename}' is not registered. Please register it first.",
                execution_duration_ms=round(elapsed_ms, 2),
            )

        file_path = registry_entry.file_path

        try:
            df = pd.read_csv(file_path)
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.error(
                "csv_read_failed",
                filename=filename,
                error=str(exc),
            )
            return ToolResult(
                data=None,
                error=f"Failed to read CSV file '{filename}'.",
                execution_duration_ms=round(elapsed_ms, 2),
            )

        # 2. Apply filters
        filters: dict | None = parameters.get("filters")
        if filters and isinstance(filters, dict):
            for col, value in filters.items():
                if col not in df.columns:
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    return ToolResult(
                        data=None,
                        error=f"Column '{col}' does not exist in '{filename}'.",
                        execution_duration_ms=round(elapsed_ms, 2),
                    )
                df = df[df[col].astype(str) == str(value)]

        # 3. Apply sorting
        sort_by: str | None = parameters.get("sort_by")
        if sort_by:
            if sort_by not in df.columns:
                elapsed_ms = (time.perf_counter() - start) * 1000
                return ToolResult(
                    data=None,
                    error=f"Sort column '{sort_by}' does not exist in '{filename}'.",
                    execution_duration_ms=round(elapsed_ms, 2),
                )
            sort_order = parameters.get("sort_order", "asc")
            ascending = sort_order != "desc"
            df = df.sort_values(by=sort_by, ascending=ascending)

        # 4. Apply aggregation (returns a single-row result)
        aggregation: dict | None = parameters.get("aggregation")
        if aggregation and isinstance(aggregation, dict):
            operation = aggregation.get("operation", "").lower()
            agg_column = aggregation.get("column", "")

            if operation not in _VALID_AGGREGATIONS:
                elapsed_ms = (time.perf_counter() - start) * 1000
                return ToolResult(
                    data=None,
                    error=(
                        f"Invalid aggregation operation '{operation}'. "
                        f"Supported: {', '.join(sorted(_VALID_AGGREGATIONS))}."
                    ),
                    execution_duration_ms=round(elapsed_ms, 2),
                )

            if operation != "count" and agg_column not in df.columns:
                elapsed_ms = (time.perf_counter() - start) * 1000
                return ToolResult(
                    data=None,
                    error=f"Aggregation column '{agg_column}' does not exist in '{filename}'.",
                    execution_duration_ms=round(elapsed_ms, 2),
                )

            try:
                if operation == "sum":
                    result_value = float(df[agg_column].sum())
                elif operation == "average":
                    result_value = float(df[agg_column].mean())
                elif operation == "count":
                    result_value = int(len(df))
                elif operation == "min":
                    result_value = float(df[agg_column].min())
                elif operation == "max":
                    result_value = float(df[agg_column].max())
                else:
                    result_value = None  # unreachable
            except (TypeError, ValueError) as exc:
                elapsed_ms = (time.perf_counter() - start) * 1000
                logger.error(
                    "csv_aggregation_failed",
                    filename=filename,
                    operation=operation,
                    column=agg_column,
                    error=str(exc),
                )
                return ToolResult(
                    data=None,
                    error=f"Aggregation '{operation}' failed on column '{agg_column}'.",
                    execution_duration_ms=round(elapsed_ms, 2),
                )

            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.info(
                "csv_aggregation_executed",
                filename=filename,
                operation=operation,
                column=agg_column,
                result=result_value,
                duration_ms=round(elapsed_ms, 2),
            )
            return ToolResult(
                data={"operation": operation, "column": agg_column, "result": result_value},
                metadata={"filename": filename, "row_count_before_agg": len(df)},
                execution_duration_ms=round(elapsed_ms, 2),
            )

        # 5. Enforce row limit and return rows
        total_rows = len(df)
        truncated = total_rows > settings.csv_row_limit
        df = df.head(settings.csv_row_limit)

        # Convert to list of dicts; handle NaN → None
        rows = df.where(df.notna(), None).to_dict(orient="records")

        elapsed_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "csv_query_executed",
            filename=filename,
            row_count=len(rows),
            truncated=truncated,
            duration_ms=round(elapsed_ms, 2),
        )

        return ToolResult(
            data=rows,
            metadata={
                "filename": filename,
                "row_count": len(rows),
                "columns": list(df.columns),
                "truncated": truncated,
            },
            execution_duration_ms=round(elapsed_ms, 2),
        )
