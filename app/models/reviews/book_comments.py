import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from app.db import Base
from app.schemas.constants import LanguageCodes

if TYPE_CHECKING:
    from ..users import User
    from ..books import Book
    from .. import Language


class BookComment(Base):
    """
    Таблица хранит пользовательские комментарии к книгам.
    """

    __tablename__ = "book_comments"

    # Первичные ключи
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), primary_key=True, nullable=False,
        comment="Идентификатор пользователя.")
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id"), primary_key=True, nullable=False,
        comment="Идентификатор книги.")

    # Значения
    language_code: Mapped["LanguageCodes"] = mapped_column(
        ForeignKey("languages.language_code"), default=LanguageCodes.UNDEFINED, nullable=False,
        comment="Отвечает за локализацию."
    )
    message: Mapped[str] = mapped_column(
        nullable=False, comment="Содержимое комментария."
    )

    # Связи
    user: Mapped["User"] = relationship(lazy="selectin", back_populates="book_comments")
    book: Mapped["Book"] = relationship(lazy="selectin", back_populates="book_comments")
    language: Mapped["Language"] = relationship(lazy="selectin", back_populates="book_comments")

    def __repr__(self):
        return f"<BookComment(user_id = '{self.user_id}', book_id = '{self.book_id}')>"
