"""Data ingestion API routes."""

from __future__ import annotations

import os
import tempfile

import structlog
from fastapi import APIRouter, Depends, UploadFile

from app.auth.dependencies import get_current_user
from app.models.errors import IngestionError
from app.services.ingestion import IngestionService

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/api/ingest", tags=["ingestion"])

_ingestion_service = IngestionService()


async def _save_upload(upload: UploadFile, suffix: str) -> str:
    """Save an uploaded file to a temporary path and return the path."""
    content = await upload.read()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(content)
    tmp.close()
    return tmp.name


@router.post("/csv")
async def ingest_csv(file: UploadFile, user: dict = Depends(get_current_user)):
    """Upload a CSV file and ingest it into the SQL database."""
    if not file.filename or not file.filename.endswith(".csv"):
        raise IngestionError("File must be a .csv file.")

    tmp_path = await _save_upload(file, suffix=".csv")
    try:
        report = _ingestion_service.ingest_csv_to_db(tmp_path, table_name=None)
    finally:
        os.unlink(tmp_path)

    return report.model_dump()


@router.post("/pdf")
async def ingest_pdf(file: UploadFile, user: dict = Depends(get_current_user)):
    """Upload a PDF file and index it for retrieval."""
    if not file.filename or not file.filename.endswith(".pdf"):
        raise IngestionError("File must be a .pdf file.")

    tmp_path = await _save_upload(file, suffix=".pdf")
    try:
        result = _ingestion_service.ingest_pdf(tmp_path)
    finally:
        os.unlink(tmp_path)

    if "error" in result:
        raise IngestionError(result["error"])

    return result


@router.post("/csv-register")
async def register_csv(file: UploadFile, user: dict = Depends(get_current_user)):
    """Upload a CSV file and register it for direct querying."""
    if not file.filename or not file.filename.endswith(".csv"):
        raise IngestionError("File must be a .csv file.")

    tmp_path = await _save_upload(file, suffix=".csv")
    try:
        result = _ingestion_service.register_csv(tmp_path)
    finally:
        os.unlink(tmp_path)

    if "error" in result:
        raise IngestionError(result["error"])

    return result
