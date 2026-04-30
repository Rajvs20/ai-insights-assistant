"""SQLAlchemy ORM models for all database tables."""

from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all ORM models."""


# ---------------------------------------------------------------------------
# Entertainment data tables (loaded from CSV seed files)
# ---------------------------------------------------------------------------


class Movie(Base):
    """Movies table."""

    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    genre: Mapped[str] = mapped_column(Text, nullable=False)
    release_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    budget: Mapped[float | None] = mapped_column(Float, nullable=True)
    revenue: Mapped[float | None] = mapped_column(Float, nullable=True)
    director: Mapped[str | None] = mapped_column(Text, nullable=True)
    studio: Mapped[str | None] = mapped_column(Text, nullable=True)


class Viewer(Base):
    """Viewers table."""

    __tablename__ = "viewers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    viewer_id: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender: Mapped[str | None] = mapped_column(Text, nullable=True)
    region: Mapped[str] = mapped_column(Text, nullable=False)
    subscription_tier: Mapped[str | None] = mapped_column(Text, nullable=True)
    signup_date: Mapped[date | None] = mapped_column(Date, nullable=True)


class WatchActivity(Base):
    """Watch activity table."""

    __tablename__ = "watch_activity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    viewer_id: Mapped[str] = mapped_column(Text, nullable=False)
    movie_id: Mapped[int] = mapped_column(Integer, nullable=False)
    watch_date: Mapped[date] = mapped_column(Date, nullable=False)
    watch_duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    device: Mapped[str | None] = mapped_column(Text, nullable=True)


class Review(Base):
    """Reviews table."""

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    viewer_id: Mapped[str] = mapped_column(Text, nullable=False)
    movie_id: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    review_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    review_date: Mapped[date] = mapped_column(Date, nullable=False)


class MarketingSpend(Base):
    """Marketing spend table."""

    __tablename__ = "marketing_spend"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(Integer, nullable=False)
    campaign_name: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[str] = mapped_column(Text, nullable=False)
    spend_amount: Mapped[float] = mapped_column(Float, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    impressions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    clicks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    conversions: Mapped[int | None] = mapped_column(Integer, nullable=True)


class RegionalPerformance(Base):
    """Regional performance table."""

    __tablename__ = "regional_performance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(Integer, nullable=False)
    region: Mapped[str] = mapped_column(Text, nullable=False)
    views: Mapped[int] = mapped_column(Integer, nullable=False)
    revenue: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)


# ---------------------------------------------------------------------------
# PDF document metadata
# ---------------------------------------------------------------------------


class PDFDocument(Base):
    """PDF document metadata table."""

    __tablename__ = "pdf_documents"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    filename: Mapped[str] = mapped_column(Text, nullable=False)
    upload_timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    chunk_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


# ---------------------------------------------------------------------------
# CSV file registry
# ---------------------------------------------------------------------------


class CSVRegistry(Base):
    """CSV file registry table."""

    __tablename__ = "csv_registry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    column_names: Mapped[str] = mapped_column(Text, nullable=False)  # JSON array
    row_count: Mapped[int] = mapped_column(Integer, nullable=False)
    registration_timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    file_path: Mapped[str] = mapped_column(Text, nullable=False)


# ---------------------------------------------------------------------------
# Schema initialisation
# ---------------------------------------------------------------------------


def create_tables() -> None:
    """Create all tables in the database.

    Uses the engine configured in :mod:`app.models.database`.
    """
    from app.models.database import engine

    Base.metadata.create_all(bind=engine)
