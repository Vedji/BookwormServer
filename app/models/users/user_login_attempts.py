from sqlalchemy import ForeignKey, func, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from datetime import datetime
from app.db import Base

if TYPE_CHECKING:
    from . import User


class UserLoginAttempts(Base):
    """
    Таблица логов попыток входа пользователей.
    """

    __tablename__ = "user_login_attempts"

    attempt_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Идентификатор попытки входа.")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False, comment="Идентификатор пользователя.")
    attempt_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), comment="Время попытки входа.")
    is_success: Mapped[bool] = mapped_column(
        nullable=False, comment="Была ли попытка входа успешна?")
    ip_address: Mapped[str] = mapped_column(
        String(45), nullable=True, comment="IP-адрес, с которого совершена попытка.")

    user: Mapped["User"] = relationship(
        lazy="selectin", foreign_keys=[user_id], back_populates="user_login_attempt", uselist=False
    )
