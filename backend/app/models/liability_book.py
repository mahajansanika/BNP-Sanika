"""`liability_book` table. Owner: Dev 2."""
from app.core.db import Base
from app.models.book_common import BookColumns


class LiabilityBook(BookColumns, Base):
    __tablename__ = "liability_book"