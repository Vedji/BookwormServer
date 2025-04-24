from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from app.db import Base
from app.schemas.constants import PasswordEncryptionTypes

if TYPE_CHECKING:
    from . import User
    from .. import File


class UserDetails(Base):
    __tablename__ = "user_details"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True, nullable=False,
        comment="Идентификатор пользователя в БД."
    )

    description: Mapped[str] = mapped_column(
        Text, nullable=True,
        comment="Описание профиля пользователя."
    )

    profile_image_id: Mapped[int] = mapped_column(
        ForeignKey("files.file_id", ondelete="SET NULL"), nullable=True,
        comment="URL изображения профиля."
    )

    user: Mapped["User"] = relationship(lazy="selectin", back_populates="details", uselist=False)
    profile_image: Mapped["File"] = relationship(lazy="selectin", back_populates="user_details", uselist=False)
