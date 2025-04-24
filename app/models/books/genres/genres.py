from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING, List

from app.db import Base

if TYPE_CHECKING:
    from . import GenreTranslation, BookGenre


class Genre(Base):
    """
    Таблица хранить идентификаторы жанров.
    """

    __tablename__ = "genres"

    genre_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Идентификатор жанра."
    )

    genre_translations: Mapped[List["GenreTranslation"]] = relationship(lazy="selectin", back_populates="genre")
    book_genres: Mapped[List["BookGenre"]] = relationship(lazy="selectin", back_populates="genre")

    def __repr__(self):
        return f"<Genre(genre_id = '{self.genre_id}')>"
