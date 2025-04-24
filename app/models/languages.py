from sqlalchemy import (String)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List, TYPE_CHECKING

from app.db import Base
from app.schemas.constants import LanguageCodes


if TYPE_CHECKING:
    from .books.genres import GenreTranslation
    from .books import BookTranslation
    from .reviews import BookComment


class Language(Base):
    __tablename__ = "languages"

    language_code: Mapped["LanguageCodes"] = mapped_column(
        String(6), primary_key=True, nullable=False, unique=True,
        comment="Языковой код ('en', 'ru' и т.п.), также является идентификатором языка в БД.")
    language_name: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="Название языка"
    )

    book_translations: Mapped[List["BookTranslation"]] = relationship(
        lazy="selectin", back_populates="language")
    genre_translations: Mapped[List["GenreTranslation"]] = relationship(
        lazy="selectin", back_populates="language")
    book_comments: Mapped[List["BookComment"]] = relationship(
        lazy="selectin", back_populates="language")

    def __repr__(self):
        return (f"<Language("
                f" language_code = '{self.language_code}',"
                f" language_name = '{self.language_name}')>")
