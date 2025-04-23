from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from app.db import Base

if TYPE_CHECKING:
    from . import Authors
    from ....books import Book


class BookAuthors(Base):
    """
    Таблица хранит список книг, которые опубликованы авторами.
    """

    __tablename__ = "book_authors"

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.author_id"), primary_key=True, nullable=False, comment="Идентификатор автора.")
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id"), primary_key=True, nullable=False, comment="Идентификатор книги."
    )

    author: Mapped["Authors"] = relationship(lazy="selectin", back_populates="books", uselist=False)
    book: Mapped["Book"] = relationship(lazy="selectin", back_populates="author", uselist=False)

    def __repr__(self):
        return (f"<models.users.roles.author.BookAuthors("
                f"author_id='{self.author_id}', book_id='{self.book_id}')>")
