"""`asset_book` table. Owner: Dev 2."""
from app.core.db import Base
from app.models.book_common import BookColumns


class AssetBook(BookColumns, Base):
    __tablename__ = "asset_book"