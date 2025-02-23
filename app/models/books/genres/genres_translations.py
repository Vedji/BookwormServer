from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from app.db import Base
from app.schemas.constants import LanguageCodes

if TYPE_CHECKING:
    from . import Genre
    from ... import Language


class GenreTranslation(Base):
    """
    Таблица хранит локализованное описание жанров.
    """

    __tablename__ = "genre_translations"

    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.genre_id"), primary_key=True, nullable=False,
        comment="Идентификатор жанра.")
    language_code: Mapped["LanguageCodes"] = mapped_column(
        ForeignKey("languages.language_code"), primary_key=True, nullable=False,
        comment="Идентификатор языка.")
    genre_name: Mapped[str] = mapped_column(
        String(255), nullable=False,
        comment="Название жанра.")

    language: Mapped["Language"] = relationship(lazy="selectin", back_populates="genre_translations", uselist=False)
    genre: Mapped["Genre"] = relationship(lazy="selectin", back_populates="genre_translations", uselist=False)

    def __repr__(self):
        return (f"<GenreTranslation("
                f"genre_id = '{self.genre_id}', "
                f"language_code = '{self.language_code}', "
                f"genre_name = '{self.genre_name}')>")
