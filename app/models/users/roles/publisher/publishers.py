from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING, List
from datetime import datetime
from app.db import Base

if TYPE_CHECKING:
    from . import PublisherCurators, BookPublishers


class Publishers(Base):
    """
    Таблица ассоциаций кураторов издательств.
    """

    __tablename__ = "publishers"

    publisher_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Уникальный идентификатор издателя.")

    publisher_name: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Название издателя.")
    website: Mapped[str] = mapped_column(
        String(1025), nullable=True, comment="Ссылка на персональный сайт издателя (Если есть).")
    contact_email: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Почтовый адрес издателя.")
    contact_phone: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="Телефонный номер для связи с издателем.")
    founded_year: Mapped[datetime] = mapped_column(
        nullable=False, comment="Дата основания издательства.")
    description: Mapped[str] = mapped_column(
        nullable=False, comment="Описание издательства.")

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), comment="Дата создания издательства в БД.")

    publisher_curators: Mapped[List["PublisherCurators"]] = relationship(lazy="selectin", back_populates="publisher")
    books: Mapped[List["BookPublishers"]] = relationship(lazy="selectin", back_populates="publisher")

    def __repr__(self):
        return (f"<models.users.roles.publisher.Publishers("
                f"publisher_id='{self.publisher_id}', "
                f"publisher_name='{self.publisher_name}')>")
