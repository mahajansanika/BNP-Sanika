from pathlib import Path

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.db import Base
from app.ingestion.service import ingest
from app.models.asset_book import AssetBook
from app.models.historical_log import HistoricalLog
from app.models.ingestion_error import IngestionError
from app.models.ingestion_run import IngestionRun
from app.models.liability_book import LiabilityBook

SEED = Path(__file__).resolve().parents[2] / "seed"
MY_TABLES = [IngestionRun.__table__, IngestionError.__table__, AssetBook.__table__,
             LiabilityBook.__table__, HistoricalLog.__table__]


@pytest.fixture()
def db():
    engine = create_engine("sqlite://", poolclass=StaticPool,
                           connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine, tables=MY_TABLES)
    with sessionmaker(engine)() as session:
        yield session


def count(db, model):
    return db.scalar(select(func.count()).select_from(model))


@pytest.mark.parametrize("sheet,fname,model", [
    ("asset", "seed_asset.csv", AssetBook),
    ("liability", "seed_liability.csv", LiabilityBook),
    ("historical", "seed_historical.csv", HistoricalLog),
])
def test_seed_upload(db, sheet, fname, model):
    run = ingest(db, sheet, fname, (SEED / fname).read_bytes())
    assert (run.status, run.rows_read, run.rows_accepted, run.rows_rejected) == ("partial", 10, 8, 2)
    assert count(db, model) == 8
    assert count(db, IngestionError) == 2
    row = db.scalars(select(model)).first()
    assert row.tenor_days >= 0 and row.cashflow >= row.amount


def test_reupload_replaces_rows(db):
    content = (SEED / "seed_historical.csv").read_bytes()
    ingest(db, "historical", "seed_historical.csv", content)
    ingest(db, "historical", "seed_historical.csv", content)
    assert count(db, HistoricalLog) == 8          # not 16


def test_bad_header_rejects_whole_file(db):
    run = ingest(db, "asset", "bad.csv", b"a,b\n1,2\n")
    assert run.status == "failed" and run.file_error
    assert count(db, AssetBook) == 0