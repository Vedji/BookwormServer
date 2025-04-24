from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import TYPE_CHECKING

from app.db import Base
from app.schemas.constants import AllowedBookFileFormats

if TYPE_CHECKING:
    from ... import User
    from ....books import Book
    from . import BookmarkEPUB, BookmarkFB2


class UserBookmark(Base):
    """
    Таблица хранить закладки пользователей в книгах.
    """

    __tablename__ = "user_bookmarks"

    bookmark_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Идентификатор книжной закладки."
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False, comment="Идентификатор пользователя."
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id"), nullable=False, comment="Идентификатор книги."
    )
    bookmark: Mapped[int] = mapped_column(
        nullable=True, default=0, comment="Позиция в тексте."
    )
    book_file_type: Mapped[AllowedBookFileFormats] = mapped_column(
        nullable=False, comment="Тип файла книги, к которому относиться закладка."
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(),
        comment="Время создания закладки."
    )

    user: Mapped["User"] = relationship(lazy="selectin", back_populates="user_bookmarks")
    book: Mapped["Book"] = relationship(lazy="selectin", back_populates="user_bookmarks")

    bookmark_epub: Mapped["BookmarkEPUB"] = relationship(
        lazy="selectin", back_populates="user_bookmark", cascade="all, delete", passive_deletes=True)
    bookmark_fb2: Mapped["BookmarkFB2"] = relationship(
        lazy="selectin", back_populates="user_bookmark", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return (f"<UserBookmark("
                f"bookmark_id = '{self.bookmark_id}', "
                f"user_id = '{self.user_id}', "
                f"book_id = '{self.book_id}')>")
