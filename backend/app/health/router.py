"""`GET /health` — liveness only. Owner: Dev 6.

Does not touch the database (`/health/db` is planned for G3) and never
requires authentication.
"""
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


@router.get("/health", response_model=HealthResponse, summary="API liveness check")
def health() -> HealthResponse:
    return HealthResponse()
