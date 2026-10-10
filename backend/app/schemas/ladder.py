"""Liquidity ladder schemas.

Owner: Dev 3. Initial contract created by Dev 6 at G1 and used by
`GET /api/v1/fixtures/ladder`. Dev 3 may ADD fields/schemas here, but the field
names and rules below are the frozen G1 contract that Dev 1 builds against.
"""
from datetime import date

from pydantic import BaseModel, Field, model_validator

from app.schemas.common import (
    BUCKET_ORDER,
    TWO_PLACES,
    Approach,
    Currency,
    Location,
    MaturityBucket,
    Money,
)


class LadderBucket(BaseModel):
    bucket: MaturityBucket
    assets: Money
    liabilities: Money
    net_gap: Money = Field(description="assets - liabilities")
    transaction_count: int = Field(ge=0)

    @model_validator(mode="after")
    def _check_net_gap(self) -> "LadderBucket":
        if abs((self.assets - self.liabilities) - self.net_gap) > TWO_PLACES / 2:
            raise ValueError(
                f"net_gap for bucket {self.bucket.value} must equal assets - liabilities"
            )
        return self


class LadderResponse(BaseModel):
    calc_date: date
    currency: Currency
    location: Location
    approach: Approach
    run_id: str
    buckets: list[LadderBucket] = Field(min_length=5, max_length=5)

    @model_validator(mode="after")
    def _check_bucket_order(self) -> "LadderResponse":
        if tuple(b.bucket for b in self.buckets) != BUCKET_ORDER:
            expected = ", ".join(b.value for b in BUCKET_ORDER)
            raise ValueError(f"buckets must be exactly [{expected}] in that order")
        return self

