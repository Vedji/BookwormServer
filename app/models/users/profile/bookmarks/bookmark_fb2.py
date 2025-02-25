from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from app.db import Base

if TYPE_CHECKING:
    from . import UserBookmark


class BookmarkFB2(Base):
    """
    Таблица закладок для книг в формате `FB2`.
    """

    __tablename__ = "bookmark_fb2"

    bookmark_id: Mapped[int] = mapped_column(
        ForeignKey("user_bookmarks.bookmark_id", ondelete="CASCADE"), primary_key=True, nullable=False,
        comment="Идентификатор закладки, к которой относится запись."
    )
    position: Mapped[int] = mapped_column(
        nullable=False, comment="Позиция в тексте на закладку."
    )

    user_bookmark: Mapped["UserBookmark"] = relationship(
        lazy="selectin", back_populates="bookmark_fb2"
    )

    def __repr__(self):
        return f"<BookmarkEPUB(bookmark_id = '{self.bookmark_id}', location = '{self.location}')>"
