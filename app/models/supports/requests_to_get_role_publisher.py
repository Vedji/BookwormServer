from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from datetime import datetime
from app.db import Base

if TYPE_CHECKING:
    from . import SupportRequest


class RequestsToGetRolePublisher(Base):
    """
    Таблица запросов на получение роли издателя контента.
    """

    __tablename__ = "requests_to_get_role_publisher"

    ticked_id: Mapped[int] = mapped_column(
        ForeignKey("support_requests.ticked_id"),
        primary_key=True, nullable=False,
        comment="Идентификатор заявки в поддержку.")
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

    base_ticked: Mapped["SupportRequest"] = relationship(
        lazy="selectin", back_populates="publisher_request")

    def __repr__(self):
        return (f"<models.supports.RequestsToGetRolePublisher("
                f"ticked_id='{self.ticked_id}', publisher_name='{self.publisher_name}')>")
