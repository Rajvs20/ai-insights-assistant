"""Application startup routine: create tables, load seed data, and index documents."""

from __future__ import annotations

import glob
import os

import structlog

from app.config.settings import settings
from app.models.database import get_session
from app.models.tables import Movie, create_tables
from app.services.ingestion import IngestionService

logger = structlog.get_logger(__name__)


def _data_already_loaded() -> bool:
    """Return True if the movies table already contains rows."""
    session = get_session()
    try:
        count = session.query(Movie).count()
        return count > 0
    finally:
        session.close()


def run_startup() -> None:
    """Run all startup tasks: create tables, ingest CSVs, PDFs, and register CSVs.

    Steps:
    1. Create all database tables (idempotent).
    2. Check if data is already loaded — skip ingestion if so.
    3. Ingest CSV seed files into the database.
    4. Ingest PDF documents into ChromaDB.
    5. Register CSV files for direct querying.
    """
    logger.info("Running startup data loading")

    # 0. Ensure data directories exist
    db_dir = os.path.dirname(settings.database_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    os.makedirs(settings.data_dir, exist_ok=True)

    # 1. Ensure all tables exist
    create_tables()
    logger.info("Database tables created (or already exist)")

    # 2. Check if data is already loaded
    if _data_already_loaded():
        logger.info("Data already loaded — skipping seed ingestion")
        return

    service = IngestionService()
    csv_dir = os.path.join(settings.data_dir, "csv")
    pdf_dir = os.path.join(settings.data_dir, "pdfs")

    # 3. Ingest CSV seed files into the database
    csv_files = sorted(glob.glob(os.path.join(csv_dir, "*.csv")))
    logger.info("Found CSV seed files", count=len(csv_files))
    for csv_path in csv_files:
        report = service.ingest_csv_to_db(csv_path)
        logger.info(
            "CSV ingested to DB",
            filename=report.filename,
            rows_inserted=report.rows_inserted,
            rows_skipped=report.rows_skipped,
            errors=report.errors,
        )

    # 4. Ingest PDF documents
    pdf_files = sorted(glob.glob(os.path.join(pdf_dir, "*.pdf")))
    logger.info("Found PDF files", count=len(pdf_files))
    for pdf_path in pdf_files:
        result = service.ingest_pdf(pdf_path)
        if "error" in result:
            logger.error("PDF ingestion failed", **result)
        else:
            logger.info("PDF ingested", **result)

    # 5. Register CSV files for direct querying
    logger.info("Registering CSV files for direct querying", count=len(csv_files))
    for csv_path in csv_files:
        result = service.register_csv(csv_path)
        if "error" in result:
            logger.error("CSV registration failed", **result)
        else:
            logger.info("CSV registered", **result)

    logger.info("Startup data loading complete")
