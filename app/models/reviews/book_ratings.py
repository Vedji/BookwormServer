import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from app.db import Base

if TYPE_CHECKING:
    from ..users import User
    from ..books import Book


class BookRating(Base):
    """
    Таблица хранить пользовательские оценки для книг.
    """

    __tablename__ = "book_ratings"

    # Первичные ключи
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), primary_key=True, nullable=False,
        comment="Идентификатор пользователя.")
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id"), primary_key=True, nullable=False,
        comment="Идентификатор книги.")

    # Значения
    rating: Mapped[int] = mapped_column(
        nullable=False, default=0,
        comment="Пользовательская оценка,"
                " должно соответствовать условию: `CHECK (rating >= 0 AND rating <= 5)`.")
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default=func.now(),
        comment="Когда была поставлена оценка."
    )

    user: Mapped["User"] = relationship(lazy="selectin", back_populates="book_ratings", uselist=False)
    book: Mapped["Book"] = relationship(lazy="selectin", back_populates="book_ratings", uselist=False)

    def __repr__(self):
        return f"<BookRating(user_id = '{self.user_id}', book_id = '{self.book_id}', rating = '{self.rating}')>"