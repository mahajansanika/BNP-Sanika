"""Behavioural (AI-adjusted) ladder API router. Owner: Dev 5.

Already registered in `app/main.py` under `/api/v1` — add endpoints here and
they appear automatically; do NOT edit main.py. Final paths are
`/api/v1/behavioural/...`. Raise `app.core.errors.AppError` subclasses for errors.

G1: intentionally empty — no contract has been agreed for these endpoints yet.
"""
from fastapi import APIRouter

from app.schemas.common import ERROR_RESPONSES

router = APIRouter(prefix="/behavioural", tags=["behavioural"], responses=ERROR_RESPONSES)
