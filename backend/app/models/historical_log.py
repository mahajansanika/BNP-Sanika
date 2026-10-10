"""`historical_log` table. Owner: Dev 2. Dev 4 trains on this."""
from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models.book_common import BookColumns


class HistoricalLog(BookColumns, Base):
    __tablename__ = "historical_log"

    type: Mapped[str] = mapped_column(String(10))                            # Asset | Liability
    actual_closure_date: Mapped[date | None] = mapped_column(default=None)   # NULL = still open