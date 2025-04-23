from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from datetime import datetime
from app.db import Base

if TYPE_CHECKING:
    from . import SupportRequest


class RequestsToGetRoleAuthor(Base):
    """
    Таблица запросов на получение роли автора контента.
    """

    __tablename__ = "requests_to_get_role_author"

    ticked_id: Mapped[int] = mapped_column(
        ForeignKey("support_requests.ticked_id"),
        primary_key=True, nullable=False,
        comment="Идентификатор заявки в поддержку.")
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

    base_ticked: Mapped["SupportRequest"] = relationship(
        lazy="selectin", back_populates="author_request"
    )

    def __repr__(self):
        return (f"<models.supports.RequestsToGetRoleAuthor("
                f"ticked_id='{self.ticked_id}', contact_email='{self.contact_email}')>")
