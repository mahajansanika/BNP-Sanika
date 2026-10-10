import os
import tempfile
from datetime import date
from pathlib import Path

from sqlalchemy import delete, insert
from sqlalchemy.orm import Session

from app.ingestion.cashflow import add_cashflows
from app.ingestion.parsers import HeaderError, read_sheet
from app.ingestion.rules import SHEETS
from app.ingestion.validator import validate_rows
from app.models.asset_book import AssetBook
from app.models.historical_log import HistoricalLog
from app.models.ingestion_error import IngestionError
from app.models.ingestion_run import IngestionRun
from app.models.liability_book import LiabilityBook

MODELS = {"asset": AssetBook, "liability": LiabilityBook, "historical": HistoricalLog}


def _record(sheet: str, c: dict, run_id: int) -> dict:
    cfg = SHEETS[sheet]
    rec = {
        "run_id": run_id,
        "transaction_id": c["Transaction_ID"],
        "entity": c["Entity"],
        "location": c["Location"],
        "customer_id": c["Customer_ID"],
        "amount": c["principal"],
        "currency": c["Currency"],
        "transaction_date": date.fromisoformat(c["Transaction_Date"]),
        "maturity_date": date.fromisoformat(c[cfg["maturity"]]),
        "interest_rate_pct": float(c["Interest_Rate_Pct"]),
        "market_interest_rate_pct": float(c["Market_Interest_Rate_Pct"]),
        "product_type": c[cfg["product"]],
        "customer_segment": c["Customer_Segment"],
        "client_rating": int(c["Client_Rating"]),
        "tenor_days": c["tenor_days"],
        "interest_amount": c["interest_amount"],
        "cashflow": c["cashflow"],
    }
    if sheet == "historical":
        rec["type"] = c["Type"].strip().capitalize()
        closed = c["Actual_Closure_Date"]
        rec["actual_closure_date"] = date.fromisoformat(closed) if closed else None
    return rec


def _read_upload(sheet: str, filename: str, content: bytes):
    suffix = Path(filename).suffix.lower()
    fd, tmp = tempfile.mkstemp(suffix=suffix)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(content)
        return read_sheet(tmp, sheet)
    finally:
        os.remove(tmp)


def ingest(db: Session, sheet: str, filename: str, content: bytes) -> IngestionRun:
    """One upload = one ingestion run. Valid rows replace the sheet's table;
    rejected rows are recorded as errors on the run."""
    run = IngestionRun(sheet=sheet, filename=filename, status="failed")
    db.add(run)
    db.flush()  # gives run.id

    try:
        rows = _read_upload(sheet, filename, content)
    except HeaderError as e:                       # R0: reject whole file
        run.file_error = str(e)
        db.commit()
        return run
    except Exception as e:                         # unreadable / unsupported file
        run.file_error = f"Could not read file: {e}"
        db.commit()
        return run

    valid, errors = validate_rows(sheet, rows)
    cash = add_cashflows(sheet, valid)

    run.rows_read = len(rows)
    run.rows_accepted = len(valid)
    run.rows_rejected = len({e["row"] for e in errors})
    run.errors_total = len(errors)
    if not errors:
        run.status = "success"
    elif valid:
        run.status = "partial"
    else:
        run.status = "failed"

    if errors:
        db.execute(insert(IngestionError), [{"run_id": run.id, **e} for e in errors])

    if valid:
        model = MODELS[sheet]
        db.execute(delete(model))                  # latest accepted upload replaces the sheet
        db.execute(insert(model), [_record(sheet, c, run.id) for c in cash])

    db.commit()
    return run