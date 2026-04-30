"""Data source listing API routes."""

from __future__ import annotations

import json

import structlog
from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.models.database import get_session
from app.models.tables import CSVRegistry, PDFDocument

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/api/data", tags=["data"])


@router.get("/sources")
async def list_data_sources(user: dict = Depends(get_current_user)):
    """Return available data sources (SQL tables, PDFs, registered CSVs)."""
    session = get_session()
    try:
        # SQL tables are always available
        sql_tables = [
            "movies",
            "viewers",
            "watch_activity",
            "reviews",
            "marketing_spend",
            "regional_performance",
        ]

        # Registered CSVs
        csv_entries = session.query(CSVRegistry).all()
        csv_sources = [
            {
                "filename": entry.filename,
                "columns": json.loads(entry.column_names),
                "row_count": entry.row_count,
            }
            for entry in csv_entries
        ]

        # Indexed PDFs
        pdf_entries = session.query(PDFDocument).all()
        pdf_sources = [
            {
                "filename": entry.filename,
                "chunk_count": entry.chunk_count,
            }
            for entry in pdf_entries
        ]
    finally:
        session.close()

    return {
        "sql_tables": sql_tables,
        "csv_files": csv_sources,
        "pdf_documents": pdf_sources,
    }
