from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from app.db import Base
from app.schemas.constants import PasswordEncryptionTypes

if TYPE_CHECKING:
    from . import User


class UserCredentials(Base):
    __tablename__ = "user_credentials"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), primary_key=True, nullable=False,
        comment="Идентификатор пользователя в БД."
    )
    email: Mapped[str] = mapped_column(
        String(256), unique=True, nullable=False,
        comment="Почта пользователя."
    )
    password_hash: Mapped[str] = mapped_column(
        String(256), nullable=False,
        comment="Зашифрованный пароль пользователя."
    )
    password_encryption: Mapped[PasswordEncryptionTypes] = mapped_column(
        default=PasswordEncryptionTypes.NONE, nullable=False,
        comment="Тип шифрования пароля."
    )

    user: Mapped["User"] = relationship(lazy="selectin", back_populates="credentials")

    def __repr__(self):
        return f"<models.UserCredentials(user_id='{self.user_id}', email='{self.email}', password_encryption='{self.password_encryption}')>"
