"""Data ingestion service for CSV and PDF files.

Handles:
- CSV-to-database ingestion with column validation and error handling
- PDF ingestion: text extraction, chunking, vector embedding storage in ChromaDB
- CSV file registration for direct querying
"""

from __future__ import annotations

import csv
import json
import os
import uuid
from datetime import date, datetime
from pathlib import Path

import chromadb
import fitz  # PyMuPDF
import structlog

from app.config.settings import settings
from app.models.database import get_session
from app.models.responses import IngestionReport
from app.models.tables import (
    Base,
    CSVRegistry,
    MarketingSpend,
    Movie,
    PDFDocument,
    RegionalPerformance,
    Review,
    Viewer,
    WatchActivity,
)

logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Column-to-model mapping
# ---------------------------------------------------------------------------

# Required columns per table (columns that are NOT NULL and have no default)
TABLE_REQUIRED_COLUMNS: dict[str, list[str]] = {
    "movies": ["title", "genre"],
    "viewers": ["viewer_id", "name", "region"],
    "watch_activity": ["viewer_id", "movie_id", "watch_date"],
    "reviews": ["viewer_id", "movie_id", "rating", "review_date"],
    "marketing_spend": [
        "movie_id",
        "campaign_name",
        "channel",
        "spend_amount",
        "start_date",
        "end_date",
    ],
    "regional_performance": [
        "movie_id",
        "region",
        "views",
        "period_start",
        "period_end",
    ],
}

# Map CSV filename stems to (SQLAlchemy model class, table_name)
FILENAME_TO_MODEL: dict[str, type[Base]] = {
    "movies": Movie,
    "viewers": Viewer,
    "watch_activity": WatchActivity,
    "reviews": Review,
    "marketing_spend": MarketingSpend,
    "regional_performance": RegionalPerformance,
}


# ---------------------------------------------------------------------------
# Row parsing helpers
# ---------------------------------------------------------------------------


def _parse_date(value: str) -> date | None:
    """Parse a date string in YYYY-MM-DD format, returning *None* on failure."""
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _parse_int(value: str) -> int | None:
    """Parse an integer string, returning *None* on failure."""
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _parse_float(value: str) -> float | None:
    """Parse a float string, returning *None* on failure."""
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _parse_bool(value: str) -> bool | None:
    """Parse a boolean string, returning *None* on failure."""
    if not value:
        return None
    lower = value.strip().lower()
    if lower in ("true", "1", "yes"):
        return True
    if lower in ("false", "0", "no"):
        return False
    return None


def _parse_movie_row(row: dict[str, str]) -> Movie | None:
    """Parse a CSV row dict into a Movie instance, or *None* if invalid."""
    title = row.get("title", "").strip()
    genre = row.get("genre", "").strip()
    if not title or not genre:
        return None
    return Movie(
        title=title,
        genre=genre,
        release_date=_parse_date(row.get("release_date", "")),
        duration_minutes=_parse_int(row.get("duration_minutes", "")),
        rating=_parse_float(row.get("rating", "")),
        budget=_parse_float(row.get("budget", "")),
        revenue=_parse_float(row.get("revenue", "")),
        director=row.get("director", "").strip() or None,
        studio=row.get("studio", "").strip() or None,
    )


def _parse_viewer_row(row: dict[str, str]) -> Viewer | None:
    viewer_id = row.get("viewer_id", "").strip()
    name = row.get("name", "").strip()
    region = row.get("region", "").strip()
    if not viewer_id or not name or not region:
        return None
    return Viewer(
        viewer_id=viewer_id,
        name=name,
        age=_parse_int(row.get("age", "")),
        gender=row.get("gender", "").strip() or None,
        region=region,
        subscription_tier=row.get("subscription_tier", "").strip() or None,
        signup_date=_parse_date(row.get("signup_date", "")),
    )


def _parse_watch_activity_row(row: dict[str, str]) -> WatchActivity | None:
    viewer_id = row.get("viewer_id", "").strip()
    movie_id = _parse_int(row.get("movie_id", ""))
    watch_date = _parse_date(row.get("watch_date", ""))
    if not viewer_id or movie_id is None or watch_date is None:
        return None
    return WatchActivity(
        viewer_id=viewer_id,
        movie_id=movie_id,
        watch_date=watch_date,
        watch_duration_minutes=_parse_int(row.get("watch_duration_minutes", "")),
        completed=_parse_bool(row.get("completed", "")),
        device=row.get("device", "").strip() or None,
    )


def _parse_review_row(row: dict[str, str]) -> Review | None:
    viewer_id = row.get("viewer_id", "").strip()
    movie_id = _parse_int(row.get("movie_id", ""))
    rating = _parse_float(row.get("rating", ""))
    review_date = _parse_date(row.get("review_date", ""))
    if not viewer_id or movie_id is None or rating is None or review_date is None:
        return None
    return Review(
        viewer_id=viewer_id,
        movie_id=movie_id,
        rating=rating,
        review_text=row.get("review_text", "").strip() or None,
        review_date=review_date,
    )


def _parse_marketing_spend_row(row: dict[str, str]) -> MarketingSpend | None:
    movie_id = _parse_int(row.get("movie_id", ""))
    campaign_name = row.get("campaign_name", "").strip()
    channel = row.get("channel", "").strip()
    spend_amount = _parse_float(row.get("spend_amount", ""))
    start_date = _parse_date(row.get("start_date", ""))
    end_date = _parse_date(row.get("end_date", ""))
    if (
        movie_id is None
        or not campaign_name
        or not channel
        or spend_amount is None
        or start_date is None
        or end_date is None
    ):
        return None
    return MarketingSpend(
        movie_id=movie_id,
        campaign_name=campaign_name,
        channel=channel,
        spend_amount=spend_amount,
        start_date=start_date,
        end_date=end_date,
        impressions=_parse_int(row.get("impressions", "")),
        clicks=_parse_int(row.get("clicks", "")),
        conversions=_parse_int(row.get("conversions", "")),
    )


def _parse_regional_performance_row(
    row: dict[str, str],
) -> RegionalPerformance | None:
    movie_id = _parse_int(row.get("movie_id", ""))
    region = row.get("region", "").strip()
    views = _parse_int(row.get("views", ""))
    period_start = _parse_date(row.get("period_start", ""))
    period_end = _parse_date(row.get("period_end", ""))
    if (
        movie_id is None
        or not region
        or views is None
        or period_start is None
        or period_end is None
    ):
        return None
    return RegionalPerformance(
        movie_id=movie_id,
        region=region,
        views=views,
        revenue=_parse_float(row.get("revenue", "")),
        avg_rating=_parse_float(row.get("avg_rating", "")),
        period_start=period_start,
        period_end=period_end,
    )


ROW_PARSERS: dict[str, callable] = {
    "movies": _parse_movie_row,
    "viewers": _parse_viewer_row,
    "watch_activity": _parse_watch_activity_row,
    "reviews": _parse_review_row,
    "marketing_spend": _parse_marketing_spend_row,
    "regional_performance": _parse_regional_performance_row,
}


# ---------------------------------------------------------------------------
# Text chunking helper
# ---------------------------------------------------------------------------


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split *text* into overlapping chunks of at most *chunk_size* characters.

    Each successive chunk starts ``chunk_size - overlap`` characters after the
    previous one, so that the last *overlap* characters of one chunk appear at
    the start of the next.
    """
    if not text:
        return []
    chunks: list[str] = []
    step = max(chunk_size - overlap, 1)
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += step
    return chunks


# ---------------------------------------------------------------------------
# IngestionService
# ---------------------------------------------------------------------------


class IngestionService:
    """Handles CSV-to-DB ingestion, PDF indexing, and CSV registration."""

    def __init__(self) -> None:
        self._chroma_client: chromadb.ClientAPI | None = None

    # -- ChromaDB lazy initialisation --------------------------------------

    def _get_chroma_client(self) -> chromadb.ClientAPI:
        if self._chroma_client is None:
            persist_dir = settings.chroma_persist_dir
            os.makedirs(persist_dir, exist_ok=True)
            self._chroma_client = chromadb.PersistentClient(path=persist_dir)
        return self._chroma_client

    def _get_pdf_collection(self) -> chromadb.Collection:
        client = self._get_chroma_client()
        return client.get_or_create_collection(
            name="pdf_chunks",
        )

    # -- CSV-to-database ingestion -----------------------------------------

    def ingest_csv_to_db(
        self, file_path: str, table_name: str | None = None
    ) -> IngestionReport:
        """Ingest a CSV file into the corresponding database table.

        Parameters
        ----------
        file_path:
            Path to the CSV file.
        table_name:
            Target table name.  If *None*, the table name is derived from the
            CSV filename stem (e.g. ``movies.csv`` → ``movies``).

        Returns
        -------
        IngestionReport
            Summary with rows_inserted, rows_skipped, and errors.
        """
        path = Path(file_path)
        filename = path.name
        stem = path.stem

        if table_name is None:
            table_name = stem

        log = logger.bind(file=filename, table=table_name)

        # Resolve model and parser
        if table_name not in FILENAME_TO_MODEL:
            msg = f"No model mapping for table '{table_name}'"
            log.error(msg)
            return IngestionReport(
                filename=filename, rows_inserted=0, rows_skipped=0, errors=[msg]
            )

        parser = ROW_PARSERS[table_name]
        required_cols = TABLE_REQUIRED_COLUMNS[table_name]

        # Read CSV
        try:
            with open(path, newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                headers = reader.fieldnames or []

                # Validate required columns
                missing = [c for c in required_cols if c not in headers]
                if missing:
                    msg = (
                        f"CSV '{filename}' is missing required columns: "
                        f"{', '.join(missing)}"
                    )
                    log.error(msg)
                    return IngestionReport(
                        filename=filename,
                        rows_inserted=0,
                        rows_skipped=0,
                        errors=[msg],
                    )

                rows = list(reader)
        except Exception as exc:
            msg = f"Failed to read CSV '{filename}': {exc}"
            log.error(msg)
            return IngestionReport(
                filename=filename, rows_inserted=0, rows_skipped=0, errors=[msg]
            )

        # Parse and insert
        inserted = 0
        skipped = 0
        errors: list[str] = []
        session = get_session()
        try:
            for idx, raw_row in enumerate(rows, start=2):  # row 1 is header
                obj = parser(raw_row)
                if obj is None:
                    warn_msg = f"Row {idx} skipped – invalid data"
                    log.warning(warn_msg, row=idx)
                    errors.append(warn_msg)
                    skipped += 1
                    continue
                session.add(obj)
                inserted += 1
            session.commit()
            log.info(
                "CSV ingestion complete",
                rows_inserted=inserted,
                rows_skipped=skipped,
            )
        except Exception as exc:
            session.rollback()
            msg = f"Database error during ingestion of '{filename}': {exc}"
            log.error(msg)
            errors.append(msg)
        finally:
            session.close()

        return IngestionReport(
            filename=filename,
            rows_inserted=inserted,
            rows_skipped=skipped,
            errors=errors,
        )

    # -- PDF ingestion -----------------------------------------------------

    def ingest_pdf(self, file_path: str) -> dict:
        """Extract text from a PDF, chunk it, embed, and store in ChromaDB.

        Parameters
        ----------
        file_path:
            Path to the PDF file.

        Returns
        -------
        dict
            ``{"doc_id": ..., "filename": ..., "chunk_count": ...}`` on
            success, or ``{"error": ...}`` on failure.
        """
        path = Path(file_path)
        filename = path.name
        log = logger.bind(file=filename)

        # Extract text
        try:
            doc = fitz.open(str(path))
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            doc.close()
        except Exception as exc:
            msg = f"Failed to read PDF '{filename}': {exc}"
            log.error(msg)
            return {"error": msg}

        full_text = full_text.strip()
        if not full_text:
            msg = f"PDF '{filename}' contains no extractable text"
            log.warning(msg)
            return {"error": msg}

        # Chunk
        chunks = chunk_text(
            full_text,
            chunk_size=settings.pdf_chunk_size,
            overlap=settings.pdf_chunk_overlap,
        )
        log.info("PDF text extracted and chunked", chunk_count=len(chunks))

        # Generate a unique document ID
        doc_id = str(uuid.uuid4())

        # Store chunks in ChromaDB
        collection = self._get_pdf_collection()
        chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {"doc_id": doc_id, "filename": filename, "chunk_index": i}
            for i in range(len(chunks))
        ]

        collection.add(
            ids=chunk_ids,
            documents=chunks,
            metadatas=metadatas,
        )
        log.info("Chunks stored in ChromaDB", doc_id=doc_id)

        # Record metadata in pdf_documents table
        session = get_session()
        try:
            pdf_record = PDFDocument(
                id=doc_id,
                filename=filename,
                chunk_count=len(chunks),
            )
            session.add(pdf_record)
            session.commit()
            log.info("PDF metadata recorded", doc_id=doc_id)
        except Exception as exc:
            session.rollback()
            msg = f"Failed to record PDF metadata for '{filename}': {exc}"
            log.error(msg)
            return {"error": msg}
        finally:
            session.close()

        return {
            "doc_id": doc_id,
            "filename": filename,
            "chunk_count": len(chunks),
        }

    # -- CSV registration --------------------------------------------------

    def register_csv(self, file_path: str) -> dict:
        """Register a CSV file for direct querying.

        Parameters
        ----------
        file_path:
            Path to the CSV file.

        Returns
        -------
        dict
            ``{"filename": ..., "columns": ..., "row_count": ...}`` on
            success, or ``{"error": ...}`` on failure.
        """
        path = Path(file_path)
        filename = path.name
        log = logger.bind(file=filename)

        # Read and validate
        try:
            with open(path, newline="", encoding="utf-8") as fh:
                reader = csv.reader(fh)
                rows_iter = iter(reader)

                # Must have a header row
                try:
                    headers = next(rows_iter)
                except StopIteration:
                    msg = f"CSV '{filename}' is empty (no headers)"
                    log.warning(msg)
                    return {"error": msg}

                if not headers or all(h.strip() == "" for h in headers):
                    msg = f"CSV '{filename}' is empty (no headers)"
                    log.warning(msg)
                    return {"error": msg}

                # Must have at least one data row
                data_rows = list(rows_iter)
                if not data_rows:
                    msg = f"CSV '{filename}' contains only headers, no data rows"
                    log.warning(msg)
                    return {"error": msg}

        except Exception as exc:
            msg = f"Failed to read CSV '{filename}': {exc}"
            log.error(msg)
            return {"error": msg}

        row_count = len(data_rows)
        column_names_json = json.dumps(headers)

        # Store in csv_registry
        session = get_session()
        try:
            registry_entry = CSVRegistry(
                filename=filename,
                column_names=column_names_json,
                row_count=row_count,
                file_path=str(path.resolve()),
            )
            session.add(registry_entry)
            session.commit()
            log.info(
                "CSV registered",
                columns=headers,
                row_count=row_count,
            )
        except Exception as exc:
            session.rollback()
            msg = f"Failed to register CSV '{filename}': {exc}"
            log.error(msg)
            return {"error": msg}
        finally:
            session.close()

        return {
            "filename": filename,
            "columns": headers,
            "row_count": row_count,
        }
