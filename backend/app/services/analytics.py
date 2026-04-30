"""Analytics Generator – extracts chart data and insights from tool results.

The :class:`AnalyticsGenerator` inspects tool results for quantitative data
and produces :class:`~app.models.responses.ChartPayload` and
:class:`~app.models.responses.Insight` objects that the frontend can render.
"""

from __future__ import annotations

import re
from typing import Any

import structlog

from app.models.responses import ChartDataset, ChartPayload, Insight
from app.tools.base import ToolResult

logger = structlog.get_logger(__name__)

# Keywords that hint at chart-friendly questions
_TREND_KEYWORDS = re.compile(
    r"\b(trend|over time|monthly|weekly|daily|yearly|growth|timeline|history)\b",
    re.IGNORECASE,
)
_DISTRIBUTION_KEYWORDS = re.compile(
    r"\b(distribution|breakdown|share|proportion|percentage|split|composition)\b",
    re.IGNORECASE,
)
_COMPARISON_KEYWORDS = re.compile(
    r"\b(compare|comparison|vs|versus|top|best|worst|ranking|rank)\b",
    re.IGNORECASE,
)


def _is_numeric(value: Any) -> bool:
    """Return True if *value* can be interpreted as a number."""
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False
    return False


def _to_float(value: Any) -> float:
    """Coerce *value* to float."""
    if isinstance(value, (int, float)):
        return float(value)
    return float(str(value))


def _detect_chart_type(question: str) -> str:
    """Heuristically choose a chart type based on the question text."""
    if _TREND_KEYWORDS.search(question):
        return "line"
    if _DISTRIBUTION_KEYWORDS.search(question):
        return "pie"
    return "bar"


def _find_label_and_value_columns(
    rows: list[dict[str, Any]],
) -> tuple[str | None, str | None]:
    """Identify the best label column and numeric value column from rows.

    Returns (label_column, value_column) or (None, None) if not found.
    """
    if not rows:
        return None, None

    first_row = rows[0]
    label_col: str | None = None
    value_col: str | None = None

    for key, val in first_row.items():
        if value_col is None and _is_numeric(val):
            value_col = key
        elif label_col is None and isinstance(val, str) and not _is_numeric(val):
            label_col = key

    # If we found a value column but no label column, use the first
    # non-numeric column or fall back to row indices.
    if value_col and not label_col:
        for key, val in first_row.items():
            if key != value_col and not _is_numeric(val):
                label_col = key
                break

    return label_col, value_col


class AnalyticsGenerator:
    """Extracts chart data and insights from tool results."""

    # ------------------------------------------------------------------
    # Chart extraction
    # ------------------------------------------------------------------

    def extract_chart_data(
        self,
        tool_results: list[ToolResult],
        question: str,
    ) -> ChartPayload | None:
        """Detect quantitative data in tool results and build a chart payload.

        Returns ``None`` when no suitable quantitative data is found.
        """
        # Collect row-based data from all successful tool results
        rows: list[dict[str, Any]] = []
        for result in tool_results:
            if result.error or result.data is None:
                continue
            if isinstance(result.data, list):
                for item in result.data:
                    if isinstance(item, dict):
                        rows.append(item)
            elif isinstance(result.data, dict):
                # Single aggregation result – not directly chartable
                # unless it has multiple keys
                if len(result.data) > 1:
                    rows.append(result.data)

        if not rows:
            return None

        label_col, value_col = _find_label_and_value_columns(rows)
        if not value_col:
            return None

        # Extract labels and values
        labels: list[str] = []
        values: list[float] = []
        for row in rows:
            label = str(row.get(label_col, "")) if label_col else str(len(labels) + 1)
            val = row.get(value_col)
            if val is not None and _is_numeric(val):
                labels.append(label)
                values.append(_to_float(val))

        if not values:
            return None

        chart_type = _detect_chart_type(question)

        # Build a readable title
        value_label = value_col.replace("_", " ").title() if value_col else "Value"
        title = f"{value_label} by {label_col.replace('_', ' ').title()}" if label_col else value_label

        logger.info(
            "chart_data_extracted",
            chart_type=chart_type,
            label_count=len(labels),
            value_column=value_col,
        )

        return ChartPayload(
            chart_type=chart_type,
            title=title,
            labels=labels,
            datasets=[
                ChartDataset(label=value_label, values=values),
            ],
        )

    # ------------------------------------------------------------------
    # Insight generation
    # ------------------------------------------------------------------

    def generate_insights(self, tool_results: list[ToolResult]) -> list[Insight]:
        """Extract key metrics from tool results.

        Looks for patterns like top performers, totals, and averages
        in the returned data.
        """
        insights: list[Insight] = []

        # Collect all row-based data
        rows: list[dict[str, Any]] = []
        for result in tool_results:
            if result.error or result.data is None:
                continue
            if isinstance(result.data, list):
                for item in result.data:
                    if isinstance(item, dict):
                        rows.append(item)
            elif isinstance(result.data, dict):
                # Aggregation result
                op = result.data.get("operation")
                col = result.data.get("column")
                res = result.data.get("result")
                if op and res is not None:
                    insights.append(
                        Insight(
                            metric_name=f"{str(op).title()} of {col}",
                            metric_value=str(res),
                            description=f"The {op} of {col} across the queried data.",
                        )
                    )

        if not rows:
            return insights

        label_col, value_col = _find_label_and_value_columns(rows)
        if not value_col:
            return insights

        # Extract numeric values
        numeric_pairs: list[tuple[str, float]] = []
        for row in rows:
            val = row.get(value_col)
            if val is not None and _is_numeric(val):
                label = str(row.get(label_col, "")) if label_col else "N/A"
                numeric_pairs.append((label, _to_float(val)))

        if not numeric_pairs:
            return insights

        value_label = value_col.replace("_", " ").title()

        # Top performer
        top = max(numeric_pairs, key=lambda x: x[1])
        insights.append(
            Insight(
                metric_name="Top Performer",
                metric_value=f"{top[0]}: {top[1]:,.2f}",
                description=f"Highest {value_label} in the result set.",
            )
        )

        # Total
        total = sum(v for _, v in numeric_pairs)
        insights.append(
            Insight(
                metric_name=f"Total {value_label}",
                metric_value=f"{total:,.2f}",
                description=f"Sum of {value_label} across {len(numeric_pairs)} items.",
            )
        )

        # Average
        avg = total / len(numeric_pairs)
        insights.append(
            Insight(
                metric_name=f"Average {value_label}",
                metric_value=f"{avg:,.2f}",
                description=f"Mean {value_label} across {len(numeric_pairs)} items.",
            )
        )

        logger.info(
            "insights_generated",
            insight_count=len(insights),
        )

        return insights
