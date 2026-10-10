"""Shared API conventions (frozen at G1). Owner: Dev 6.

Do not change these values without agreement from the whole team — Dev 1's
frontend and every feature module build against them.
"""
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, PlainSerializer

from app.core.config import API_V1_PREFIX  # noqa: F401  (single source of truth)
DATE_FORMAT = "YYYY-MM-DD"  # ISO 8601 calendar date; `datetime.date` serialises to this.

TWO_PLACES = Decimal("0.01")


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    SGD = "SGD"
    HKD = "HKD"


class Location(str, Enum):
    HONG_KONG = "Hong Kong"
    NEW_YORK = "New York"
    LONDON = "London"
    SINGAPORE = "Singapore"
    PARIS = "Paris"


class MaturityBucket(str, Enum):
    M0_1 = "0-1M"
    M1_3 = "1-3M"
    M3_12 = "3-12M"
    Y1_5 = "1-5Y"
    Y5_PLUS = ">5Y"


# Canonical display/response order for ladders.
BUCKET_ORDER: tuple[MaturityBucket, ...] = tuple(MaturityBucket)


class Approach(str, Enum):
    DETERMINISTIC = "deterministic"
    AI = "ai"
    WHATIF = "whatif"


def quantize_money(value: Decimal) -> Decimal:
    return value.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def _money_to_json(value: Decimal) -> float:
    return float(quantize_money(value))


# Money: Decimal inside the backend (PostgreSQL NUMERIC), a JSON number rounded
# to two decimal places on the wire.
Money = Annotated[Decimal, PlainSerializer(_money_to_json, return_type=float, when_used="json")]

CalcDate = date


class ErrorResponse(BaseModel):
    """Body of every non-2xx response."""

    model_config = ConfigDict(json_schema_extra={
        "example": {"code": "NOT_FOUND", "message": "The requested resource was not found."}
    })

    code: str
    message: str


class LadderQueryParams(BaseModel):
    """Query parameters every ladder / drill-down endpoint accepts (G1 contract)."""

    calc_date: date
    currency: Currency
    location: Location
    run_id: str | None = None


# Standard error responses to attach to routes for OpenAPI docs.
ERROR_RESPONSES: dict[int | str, dict] = {
    400: {"model": ErrorResponse, "description": "Invalid business input"},
    401: {"model": ErrorResponse, "description": "Not authenticated"},
    403: {"model": ErrorResponse, "description": "Forbidden"},
    404: {"model": ErrorResponse, "description": "Not found"},
    500: {"model": ErrorResponse, "description": "Unexpected server error"},
}
