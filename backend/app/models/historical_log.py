"""`historical_log` table — G1 STUB. Owner: Dev 2.

Only the primary key is defined so the table name is reserved, the model is
importable and `Base.metadata` has no conflicts. Columns are intentionally
NOT invented here: the owner adds them once the schema is agreed (see
docs/schema.md). Store money as `Numeric` (Decimal), never Float.
"""
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class HistoricalLog(Base):
    __tablename__ = "historical_log"

    id: Mapped[int] = mapped_column(primary_key=True)
