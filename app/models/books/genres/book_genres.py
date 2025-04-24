from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from app.db import Base

if TYPE_CHECKING:
    from . import Genre
    from .. import Book


class BookGenre(Base):
    """
    Таблица ассоциаций между книгами и жанрами.
    """

    __tablename__ = "book_genres"

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id"), primary_key=True, nullable=False,
        comment="Идентификатор книги."
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.genre_id"), primary_key=True, nullable=False,
        comment="Идентификатор жанра."
    )

    book: Mapped["Book"] = relationship(lazy="selectin", back_populates="book_genres", uselist=False)
    genre: Mapped["Genre"] = relationship(lazy="selectin", back_populates="book_genres", uselist=False)

    def __repr__(self):
        return f"<BookGenre(book_id = '{self.book_id}', genre_id = '{self.genre_id}')>"
