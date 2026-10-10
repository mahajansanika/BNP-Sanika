"""Ingestion API schemas. Owner: Dev 2."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

Sheet = Literal["asset", "liability", "historical"]
RunStatus = Literal["success", "partial", "failed"]


class IngestionErrorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    row: int          # spreadsheet row number (header is row 1)
    column: str
    value: str
    rule: str         # "R1".."R16"
    message: str


class IngestionReport(BaseModel):
    """Returned by POST /api/v1/ingest/{assets|liabilities|historical}."""
    model_config = ConfigDict(from_attributes=True)

    run_id: int
    sheet: Sheet
    filename: str
    status: RunStatus
    rows_read: int
    rows_accepted: int
    rows_rejected: int             # number of rows, not number of errors
    file_error: str | None = None  # set when R0 rejects the whole file
    errors_total: int              # number of error records (a row can have several)
    errors: list[IngestionErrorOut] = []   # first 50 only
    created_at: datetime


class ErrorsPage(BaseModel):
    """Returned by GET /api/v1/ingest/runs/{id}/errors?offset=&limit=."""
    run_id: int
    total: int
    offset: int
    limit: int
    items: list[IngestionErrorOut]