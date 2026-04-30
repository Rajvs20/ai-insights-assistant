"""SQLAlchemy engine setup and session management."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import settings

engine = create_engine(
    f"sqlite:///{settings.database_path}",
    echo=settings.debug,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session.

    The session is automatically closed when the request finishes.

    Usage as a FastAPI dependency::

        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session() -> Session:
    """Create and return a new database session.

    Usage::

        session = get_session()
        try:
            ...
            session.commit()
        finally:
            session.close()

    Or as a context-manager with :func:`contextlib.closing`.
    """
    return SessionLocal()
