"""Columns shared by asset_book, liability_book and historical_log. Owner: Dev 2.
Names are unified on every table: amount / maturity_date / product_type."""
from datetime import date
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column


class BookColumns:
    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("ingestion_runs.id"), index=True)
    transaction_id: Mapped[str] = mapped_column(String(20), index=True)
    entity: Mapped[str] = mapped_column(String(30))
    location: Mapped[str] = mapped_column(String(30), index=True)
    customer_id: Mapped[str] = mapped_column(String(20))
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2))
    currency: Mapped[str] = mapped_column(String(3), index=True)
    transaction_date: Mapped[date]
    maturity_date: Mapped[date] = mapped_column(index=True)
    interest_rate_pct: Mapped[Decimal] = mapped_column(Numeric(7, 4))
    market_interest_rate_pct: Mapped[Decimal] = mapped_column(Numeric(7, 4))
    product_type: Mapped[str] = mapped_column(String(20))
    customer_segment: Mapped[str] = mapped_column(String(20))
    client_rating: Mapped[int]
    tenor_days: Mapped[int]
    interest_amount: Mapped[Decimal] = mapped_column(Numeric(20, 2))
    cashflow: Mapped[Decimal] = mapped_column(Numeric(20, 2))