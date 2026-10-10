"""SQLAlchemy 2.0 database foundation. Owner: Dev 6.

The engine is created lazily-connecting: importing this module (and therefore
starting the API) does NOT require PostgreSQL to be reachable. A connection is
only opened when a session is actually used.
"""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    """Declarative base shared by every model in `app.models`."""


_settings = get_settings()

engine = create_engine(
    _settings.database_url.get_secret_value(),
    pool_pre_ping=True,  # recover from dropped connections
    pool_size=5,
    max_overflow=10,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, class_=Session)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency: one session per request, always closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def create_all() -> None:
    """Create every table registered on `Base.metadata` (no Alembic in this project)."""
    import app.models  # noqa: F401  - registers all models on Base.metadata

    Base.metadata.create_all(bind=engine)
