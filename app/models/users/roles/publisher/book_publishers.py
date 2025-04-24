from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from app.db import Base

if TYPE_CHECKING:
    from . import Publishers
    from ....books import Book


class BookPublishers(Base):
    """
    Таблица хранить книги, которые опубликовали издатели.
    """

    __tablename__ = "book_publishers"

    publisher_id: Mapped[int] = mapped_column(
        ForeignKey("publishers.publisher_id"), primary_key=True, nullable=False, comment="Идентификатор издательства.")
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id"), primary_key=True, nullable=False, comment="Идентификатор книги."
    )

    book: Mapped["Book"] = relationship(lazy="selectin", back_populates="publisher", uselist=False)
    publisher: Mapped["Publishers"] = relationship(lazy="selectin", back_populates="books", uselist=False)

    def __repr__(self):
        return (f"<models.users.roles.publisher.BookPublishers("
                f"publisher_id='{self.publisher_id}', book_id='{self.book_id}')>")
