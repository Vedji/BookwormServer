from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from app.db import Base

if TYPE_CHECKING:
    from . import UserBookmark


class BookmarkEPUB(Base):
    """
    Таблица закладок для книг в формате `EPUB`.
    """

    __tablename__ = "bookmark_epub"

    bookmark_id: Mapped[int] = mapped_column(
        ForeignKey("user_bookmarks.bookmark_id", ondelete="CASCADE"), primary_key=True, nullable=False,
        comment="Идентификатор закладки, к которой относится запись."
    )
    location: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Указатель на заготовок в `EPUB`."
    )

    user_bookmark: Mapped["UserBookmark"] = relationship(
        lazy="selectin", back_populates="bookmark_epub"
    )

    def __repr__(self):
        return f"<BookmarkEPUB(bookmark_id = '{self.bookmark_id}', location = '{self.location}')>"
