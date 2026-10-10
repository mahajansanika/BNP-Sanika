"""`recommendations` table — G1 STUB. Owner: Dev 5.

Only the primary key is defined so the table name is reserved, the model is
importable and `Base.metadata` has no conflicts. Columns are intentionally
NOT invented here: the owner adds them once the schema is agreed (see
docs/schema.md). Store money as `Numeric` (Decimal), never Float.
"""
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
