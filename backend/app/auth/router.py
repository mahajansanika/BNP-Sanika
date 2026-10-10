"""Auth router (`/api/v1/auth`). Owner: Dev 6.

G1: registered but empty. `POST /api/v1/auth/login` and `GET /api/v1/auth/me`
arrive in G2 using the schemas in `app.schemas.auth`.
"""
from fastapi import APIRouter

from app.schemas.common import ERROR_RESPONSES

router = APIRouter(prefix="/auth", tags=["auth"], responses=ERROR_RESPONSES)
