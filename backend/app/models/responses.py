"""Pydantic response models used across the application."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class IngestionReport(BaseModel):
    """Report returned after CSV-to-database ingestion."""

    filename: str
    rows_inserted: int
    rows_skipped: int
    errors: list[str]


# ---------------------------------------------------------------------------
# Source attribution
# ---------------------------------------------------------------------------


class SourceAttribution(BaseModel):
    """Identifies a data source that contributed to an answer."""

    source_type: Literal["sql", "pdf", "csv"]
    source_name: str
    detail: str  # e.g., table name, document filename, CSV filename


# ---------------------------------------------------------------------------
# Chart / analytics payload
# ---------------------------------------------------------------------------


class ChartDataset(BaseModel):
    """A single dataset within a chart."""

    label: str
    values: list[float]


class ChartPayload(BaseModel):
    """Structured data for rendering a chart on the frontend."""

    chart_type: Literal["bar", "line", "pie"]
    title: str
    labels: list[str]
    datasets: list[ChartDataset]


class Insight(BaseModel):
    """A single insight extracted from tool results."""

    metric_name: str
    metric_value: str
    description: str


# ---------------------------------------------------------------------------
# Tool trace
# ---------------------------------------------------------------------------


class ToolTraceEntry(BaseModel):
    """Records a single tool invocation for auditability."""

    tool_name: str
    input_parameters: dict
    output_summary: str
    execution_duration_ms: float


# ---------------------------------------------------------------------------
# Chat response
# ---------------------------------------------------------------------------


class ChatResponse(BaseModel):
    """Full response returned by the orchestrator for a chat question."""

    answer: str
    sources: list[SourceAttribution] = Field(default_factory=list)
    chart_data: ChartPayload | None = None
    insights: list[Insight] | None = None
    tool_trace: list[ToolTraceEntry] = Field(default_factory=list)
    session_id: str
    correlation_id: str


# ---------------------------------------------------------------------------
# Error response
# ---------------------------------------------------------------------------


class ErrorResponse(BaseModel):
    """Standardised error response returned by the API."""

    error_code: str
    message: str
    correlation_id: str
