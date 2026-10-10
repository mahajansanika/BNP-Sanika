"""`ingestion_runs` table: one row per upload. Owner: Dev 2."""
from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    sheet: Mapped[str] = mapped_column(String(20))        # asset | liability | historical
    filename: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(10))       # success | partial | failed
    rows_read: Mapped[int] = mapped_column(default=0)
    rows_accepted: Mapped[int] = mapped_column(default=0)
    rows_rejected: Mapped[int] = mapped_column(default=0)
    errors_total: Mapped[int] = mapped_column(default=0)
    file_error: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())