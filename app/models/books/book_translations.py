from sqlalchemy import String, ForeignKey, Date, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
import datetime

from app.db import Base
from app.schemas.constants import LanguageCodes

if TYPE_CHECKING:
    from . import Book
    from models import Language


class BookTranslation(Base):
    """
    Таблица хранить локализации названия и описания книги.
    """

    __tablename__ = "book_translations"

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id"), primary_key=True, nullable=False,
        comment="Идентификатор книги."
    )
    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.language_code"), primary_key=True, nullable=False,
        comment="Идентификатор локализации."
    )

    book_title: Mapped[str] = mapped_column(
        String(256), nullable=False, comment="Название произведения."
    )
    book_description: Mapped[str] = mapped_column(
        nullable=True, comment="Локализация описания книги."
    )

    book: Mapped["Book"] = relationship(lazy="selectin", back_populates="book_translations", uselist=False)
    language: Mapped["Language"] = relationship(lazy="selectin", back_populates="book_translations", uselist=False)

    @staticmethod
    def create(book_id: int, language_code: LanguageCodes, book_title: str, book_description: str = None) -> "BookTranslation":
        """ Создает экземпляр класса """
        new: "BookTranslation" = BookTranslation(
            book_id = book_id,
            language_code = language_code,
            book_title = book_title
        )
        if book_description:
            new.book_description = book_description
        return new

    def __repr__(self):
        return (f"<BookTranslation("
                f"book_id = '{self.book_id}', "
                f"language_code = '{self.language_code}', "
                f"book_title = '{self.book_title}')>")
