from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING, List
from datetime import datetime
from app.db import Base

if TYPE_CHECKING:
    from . import BookAuthors, AuthorCurators


class Authors(Base):
    """
    Таблица хранит информацию об авторах книг.
    """

    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Идентификатор автора.")

    first_name: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Имя автора.")
    last_name: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Фамилия автора.")
    contact_email: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Почтовый адрес автора.")
    website: Mapped[str] = mapped_column(
        String(1025), nullable=True, comment="Ссылка на персональный сайт автора (Если есть).")
    birthday: Mapped[datetime] = mapped_column(
        nullable=True, comment="Дата рождения автора.")
    nationality: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="Страна рождения автора.")
    description: Mapped[str] = mapped_column(
        nullable=True, comment="Пара слов о авторе.")

    books: Mapped[List["BookAuthors"]] = relationship(lazy="selectin", back_populates="author")
    author_curators: Mapped["AuthorCurators"] = relationship(lazy="selectin", back_populates="author", uselist=False)

    def __repr__(self):
        return (f"<models.users.roles.publisher.Authors("
                f"author_id='{self.author_id}', "
                f"first_name='{self.first_name}', "
                f"last_name='{self.last_name}', "
                f"contact_email='{self.contact_email}')>")
