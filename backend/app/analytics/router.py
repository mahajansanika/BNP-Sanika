"""Analytics API router. Owner: Dev 4.

Already registered in `app/main.py` under `/api/v1` — add endpoints here and
they appear automatically; do NOT edit main.py. Final paths are
`/api/v1/analytics/...`. Raise `app.core.errors.AppError` subclasses for errors.

G1: intentionally empty — no contract has been agreed for these endpoints yet.
"""
from fastapi import APIRouter

from app.schemas.common import ERROR_RESPONSES

router = APIRouter(prefix="/analytics", tags=["analytics"], responses=ERROR_RESPONSES)
