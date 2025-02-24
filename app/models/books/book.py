import datetime

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING

from app.db import Base
from app.schemas.constants import AllowedBookFileFormats

if TYPE_CHECKING:
    from ..users import User
    from .. import File
    from . import BookPreviewImage, BookTranslation
    from .genres import BookGenre
    from ..reviews import BookRating, BookComment


class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Идентификатор книги.")

    book_publication_date: Mapped[datetime.datetime] = mapped_column(nullable=True, comment="Дата публикации книги.")

    book_content: Mapped[int] = mapped_column(
        ForeignKey("files.file_id"), nullable=True,
        comment="Идентификатор файла, указывающий на файл, в котором содержится содержимое книги."
    )
    book_content_type: Mapped[AllowedBookFileFormats] = mapped_column(
        nullable=False, comment="В каком формате загружено содержимое книги.")

    book_isbn: Mapped[str] = mapped_column(String(14), nullable=True, comment="ISBN код книги без разделителей.")

    added_user: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=True, comment="Идентификатор пользователя, который добавил книгу."
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default=func.now())
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default=func.now())

    # Связи
    user: Mapped["User"] = relationship(lazy="selectin", back_populates="added_books")
    content: Mapped["File"] = relationship(lazy="selectin", back_populates="books", uselist=False)
    preview_images: Mapped[List["BookPreviewImage"]] = relationship(lazy="selectin", back_populates="for_book")
    book_translations: Mapped[List["BookTranslation"]] = relationship(lazy="selectin", back_populates="book")
    book_genres: Mapped[List["BookGenre"]] = relationship(lazy="selectin", back_populates="book")
    book_ratings: Mapped[List["BookRating"]] = relationship(
        lazy="selectin", back_populates="book")
    book_comments: Mapped[List["BookComment"]] = relationship(lazy="selectin")


    def __repr__(self):
        return f"<Book(book_id='{self.book_id}')>"
