"""Router tests: SQLite in memory, no Postgres needed."""
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.db import Base, get_db
from app.main import app
from app.models.asset_book import AssetBook
from app.models.historical_log import HistoricalLog
from app.models.ingestion_error import IngestionError
from app.models.ingestion_run import IngestionRun
from app.models.liability_book import LiabilityBook

SEED = Path(__file__).resolve().parents[2] / "seed"
TABLES = [IngestionRun.__table__, IngestionError.__table__, AssetBook.__table__,
          LiabilityBook.__table__, HistoricalLog.__table__]
P = "/api/v1/ingest"


@pytest.fixture()
def api():
    engine = create_engine("sqlite://", poolclass=StaticPool,
                           connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine, tables=TABLES)
    maker = sessionmaker(engine)

    def override():
        with maker() as s:
            yield s

    app.dependency_overrides[get_db] = override
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.pop(get_db, None)


def up(api, kind, name, content):
    return api.post(f"{P}/{kind}", files={"file": (name, content)})


def test_upload_seed_returns_report(api):
    r = up(api, "assets", "seed_asset.csv", (SEED / "seed_asset.csv").read_bytes())
    assert r.status_code == 200
    b = r.json()
    assert (b["status"], b["rows_read"], b["rows_accepted"], b["rows_rejected"]) == ("partial", 10, 8, 2)
    assert b["errors_total"] == len(b["errors"]) == 2


def test_runs_list_and_detail(api):
    for kind, f in [("assets", "seed_asset.csv"), ("liabilities", "seed_liability.csv")]:
        up(api, kind, f, (SEED / f).read_bytes())
    runs = api.get(f"{P}/runs").json()
    assert [x["sheet"] for x in runs] == ["liability", "asset"]      # newest first
    assert all(x["errors"] == [] for x in runs)                     # no inline errors in list
    one = api.get(f"{P}/runs/{runs[1]['run_id']}").json()
    assert one["sheet"] == "asset" and len(one["errors"]) == 2
    assert api.get(f"{P}/runs?limit=1").json().__len__() == 1


def test_run_not_found(api):
    assert api.get(f"{P}/runs/999").status_code == 404
    assert api.get(f"{P}/runs/999/errors").status_code == 404


def test_errors_pagination(api):
    r = up(api, "historical", "seed_historical.csv", (SEED / "seed_historical.csv").read_bytes()).json()
    page = api.get(f"{P}/runs/{r['run_id']}/errors?limit=1&offset=1").json()
    assert page["total"] == 2 and len(page["items"]) == 1 and page["offset"] == 1


# ---- negative tests ----
def test_wrong_extension_400(api):
    assert up(api, "assets", "a.txt", b"x").status_code == 400


def test_unknown_kind_422(api):
    assert up(api, "loans", "a.csv", b"x").status_code == 422


def test_missing_file_422(api):
    assert api.post(f"{P}/assets").status_code == 422


def test_bad_header_is_failed_run_not_500(api):
    r = up(api, "assets", "bad.csv", b"a,b\n1,2\n")
    assert r.status_code == 200 and r.json()["status"] == "failed" and r.json()["file_error"]


def test_empty_file_is_failed_run(api):
    r = up(api, "liabilities", "empty.csv", b"")
    assert r.status_code == 200 and r.json()["status"] == "failed"


def test_corrupt_xlsx_is_failed_run(api):
    r = up(api, "historical", "corrupt.xlsx", b"this is not a zip file")
    assert r.status_code == 200 and r.json()["status"] == "failed" and r.json()["file_error"]


def test_header_only_file_is_failed_run(api):
    header = (SEED / "seed_asset.csv").read_text().splitlines()[0] + "\n"
    r = up(api, "assets", "h.csv", header.encode())
    assert r.status_code == 200 and r.json()["rows_accepted"] == 0
