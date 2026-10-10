"""`ingestion_errors` table: one row per rejected cell. Owner: Dev 2."""
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class IngestionError(Base):
    __tablename__ = "ingestion_errors"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("ingestion_runs.id", ondelete="CASCADE"), index=True)
    row: Mapped[int] = mapped_column("row_number")            # DB names avoid SQL keywords
    column: Mapped[str] = mapped_column("column_name", String(60))
    value: Mapped[str] = mapped_column(Text, default="")
    rule: Mapped[str] = mapped_column(String(5))
    message: Mapped[str] = mapped_column(String(200))