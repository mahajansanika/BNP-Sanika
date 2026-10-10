from typing import Literal

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.ingestion.service import ingest
from app.models.ingestion_error import IngestionError
from app.models.ingestion_run import IngestionRun
from app.schemas.ingestion import ErrorsPage, IngestionErrorOut, IngestionReport

router = APIRouter(prefix="/ingest", tags=["ingestion"])   # main.py mounts it under /api/v1

PATH_TO_SHEET = {"assets": "asset", "liabilities": "liability", "historical": "historical"}
ALLOWED = (".csv", ".xlsx", ".xls")
INLINE_ERRORS = 50


def _report(db: Session, run: IngestionRun, inline: int = INLINE_ERRORS) -> IngestionReport:
    first = [] if inline <= 0 else db.scalars(
        select(IngestionError).where(IngestionError.run_id == run.id)
        .order_by(IngestionError.id).limit(inline)
    ).all()
    return IngestionReport(
        run_id=run.id, sheet=run.sheet, filename=run.filename, status=run.status,
        rows_read=run.rows_read, rows_accepted=run.rows_accepted,
        rows_rejected=run.rows_rejected, file_error=run.file_error,
        errors_total=run.errors_total, created_at=run.created_at,
        errors=[IngestionErrorOut.model_validate(e) for e in first],
    )


@router.get("/runs", response_model=list[IngestionReport])
def list_runs(limit: int = 20, db: Session = Depends(get_db)):
    """Upload history, newest first. No inline errors; use /runs/{id}/errors."""
    limit = max(1, min(limit, 100))
    runs = db.scalars(select(IngestionRun).order_by(IngestionRun.id.desc()).limit(limit)).all()
    return [_report(db, r, inline=0) for r in runs]


@router.get("/runs/{run_id}", response_model=IngestionReport)
def get_run(run_id: int, db: Session = Depends(get_db)):
    run = db.get(IngestionRun, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Ingestion run not found")
    return _report(db, run)


# TODO: add the auth dependency from Dev 1/6 here (admin or analyst role only)
@router.post("/{kind}", response_model=IngestionReport)
def upload(
    kind: Literal["assets", "liabilities", "historical"],
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    name = file.filename or ""
    if not name.lower().endswith(ALLOWED):
        raise HTTPException(status_code=400, detail="Upload a .csv or .xlsx file")
    run = ingest(db, PATH_TO_SHEET[kind], name, file.file.read())
    return _report(db, run)


@router.get("/runs/{run_id}/errors", response_model=ErrorsPage)
def run_errors(run_id: int, offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    run = db.get(IngestionRun, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Ingestion run not found")
    limit = max(1, min(limit, 500))
    items = db.scalars(
        select(IngestionError).where(IngestionError.run_id == run_id)
        .order_by(IngestionError.id).offset(offset).limit(limit)
    ).all()
    return ErrorsPage(run_id=run_id, total=run.errors_total, offset=offset, limit=limit,
                      items=[IngestionErrorOut.model_validate(e) for e in items])