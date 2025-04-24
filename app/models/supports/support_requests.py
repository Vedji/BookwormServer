from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from datetime import datetime
from app.db import Base
from app.schemas.constants.ticket_attributes import RequestStatus, SupportRequestTypes

if TYPE_CHECKING:
    from ..users import User
    from . import RequestsToGetRoleAuthor, RequestsToGetRolePublisher


class SupportRequest(Base):
    """
    Таблица общих заявок пользователей на поддержку.
    """

    __tablename__ = "support_requests"

    ticked_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Идентификатор заявки в поддержку.")

    support_request_type: Mapped[SupportRequestTypes] = mapped_column(
        nullable=False,
        default=SupportRequestTypes.REQUEST_TYPE_NONE,
        comment="Тип запроса в поддержку.")
    status: Mapped[RequestStatus] = mapped_column(
        nullable=False,
        default=RequestStatus.PENDING,
        comment="Статус запроса к поддержки.")
    reviewed_at: Mapped[datetime] = mapped_column(
        nullable=True,
        default=None,
        comment="Время рассмотрения заявки.")
    subject: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Тема запроса")
    message: Mapped[str] = mapped_column(
        nullable=True,
        comment="Сообщение запроса")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False, comment="Идентификатор пользователя, который оставил заявку.")
    moderator_comment: Mapped[str] = mapped_column(nullable=True, comment="Ответ модератора.")
    reviewed_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=True, default=None, comment="Идентификатор пользователя, который рассмотрел заявку.")

    created_by: Mapped["User"] = relationship(
        lazy="selectin", foreign_keys=[user_id], back_populates="submitted_tickets", cascade="all, delete", passive_deletes=True)
    reviewed_by: Mapped["User"] = relationship(
        lazy="selectin", foreign_keys=[reviewed_user_id], back_populates="reviewed_tickets", cascade="all, delete", passive_deletes=True)

    author_request: Mapped["RequestsToGetRoleAuthor"] = relationship(
        lazy="selectin", back_populates="base_ticked", uselist=False, cascade="all, delete", passive_deletes=True
    )
    publisher_request: Mapped["RequestsToGetRolePublisher"] = relationship(
        lazy="selectin", back_populates="base_ticked", uselist=False, cascade="all, delete", passive_deletes=True
    )

    def __repr__(self):
        return (f"<models.supports.SupportRequest("
                f"ticked_id='{self.ticked_id}', "
                f"status='{self.status}', "
                f"support_request_type='{self.support_request_type}', "
                f"created_by='{self.user_id}')>")
