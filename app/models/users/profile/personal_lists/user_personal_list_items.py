from sqlalchemy import String, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List, TYPE_CHECKING

from app.db import Base


if TYPE_CHECKING:
    from . import UserPersonalList
    from ....books import Book


class UserPersonalListItem(Base):
    """
    Таблица хранить записи о добавленных книгах в пользовательские списки.
    """

    __tablename__ = "user_personal_list_items"

    # Первичные ключи
    personal_list_id: Mapped[int] = mapped_column(
        ForeignKey("user_personal_lists.personal_list_id"), primary_key=True, nullable=False,
        comment="Идентификатор пользовательского списка."
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id"), primary_key=True, nullable=False,
        comment="Идентификатор книги."
    )

    # Значение
    added_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), comment="Время добавления книги в пользовательский список."
    )

    # Связи
    personal_list: Mapped["UserPersonalList"] = relationship(
        lazy="selectin", back_populates="items")
    book: Mapped["Book"] = relationship(
        lazy="selectin", back_populates="user_personal_list_items")

    def __repr__(self):
        return f"<UserPersonalListItem(personal_list_id = '{self.personal_list_id}', book_id = '{self.book_id}')>"
