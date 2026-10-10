"""Fixture endpoints. Owner: Dev 6.

TEMPORARY & UNAUTHENTICATED (G1): serves fully synthetic data from
`backend/fixtures/` so Dev 1 can build the ladder UI before the gap engine
exists. Authentication is added in G2. The file path is fixed server-side;
no request input ever influences which file is read.
"""
import json
import logging
from decimal import Decimal
from pathlib import Path

from fastapi import APIRouter
from pydantic import ValidationError

from app.core.config import BACKEND_DIR
from app.core.errors import AppError
from app.schemas.common import ERROR_RESPONSES
from app.schemas.ladder import LadderResponse

logger = logging.getLogger(__name__)

LADDER_FIXTURE_PATH: Path = BACKEND_DIR / "fixtures" / "ladder.json"

router = APIRouter(prefix="/fixtures", tags=["fixtures"], responses=ERROR_RESPONSES)


class FixtureUnavailableError(AppError):
    status_code = 500
    code = "FIXTURE_UNAVAILABLE"
    message = "The ladder fixture is not available on the server."


class FixtureInvalidError(AppError):
    status_code = 500
    code = "FIXTURE_INVALID"
    message = "The ladder fixture on the server is invalid."


def load_ladder_fixture(path: Path | None = None) -> LadderResponse:
    path = path or LADDER_FIXTURE_PATH  # resolved at call time
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        logger.error("Ladder fixture missing: %s", path.name)
        raise FixtureUnavailableError() from exc
    except OSError as exc:
        logger.error("Ladder fixture unreadable: %s", type(exc).__name__)
        raise FixtureUnavailableError() from exc
    try:
        # parse_float=Decimal keeps money exact (no binary-float drift).
        data = json.loads(raw, parse_float=Decimal)
        return LadderResponse.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as exc:
        logger.error("Ladder fixture invalid: %s", exc)
        raise FixtureInvalidError() from exc


@router.get(
    "/ladder",
    response_model=LadderResponse,
    summary="Synthetic deterministic liquidity ladder (temporary, G1)",
)
def get_ladder_fixture() -> LadderResponse:
    return load_ladder_fixture()
