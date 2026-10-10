"""`users` table. Owner: Dev 6."""
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'support')", name="ck_users_role"),
        # Location-scoped users must have a location; Support users may have none.
        CheckConstraint("role = 'support' OR location IS NOT NULL", name="ck_users_location_scope"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))  # bcrypt hash only, never plaintext
    role: Mapped[str] = mapped_column(String(20), default="user")
    location: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:  # never include password_hash
        return f"User(id={self.id!r}, username={self.username!r}, role={self.role!r})"
