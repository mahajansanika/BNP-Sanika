"""All eleven model files import together with no metadata conflicts."""
from sqlalchemy import create_engine, inspect

EXPECTED_TABLES = {
    "users", "ingestion_runs", "ingestion_errors", "asset_book", "liability_book",
    "historical_log", "ml_models", "predictions", "gap_snapshots", "recommendations",
    "audit_log",
}


def test_all_models_register_expected_tables():
    import app.models  # noqa: F401
    from app.core.db import Base
    assert set(Base.metadata.tables) == EXPECTED_TABLES


def test_metadata_creates_cleanly_without_postgres():
    # In-memory SQLite proves the metadata is self-consistent (FKs resolve,
    # no duplicate names) without needing a live PostgreSQL server.
    import app.models  # noqa: F401
    from app.core.db import Base
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    assert set(inspect(engine).get_table_names()) == EXPECTED_TABLES


def test_db_foundation_configured():
    from sqlalchemy.orm import sessionmaker
    from app.core import db
    assert db.engine.dialect.name == "postgresql"
    assert isinstance(db.SessionLocal, sessionmaker)
    gen = db.get_db()
    session = next(gen)  # creating a session does not open a connection
    gen.close()
    assert session is not None
