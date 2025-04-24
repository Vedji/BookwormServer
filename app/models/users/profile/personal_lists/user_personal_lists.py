from sqlalchemy import String, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List, TYPE_CHECKING

from app.db import Base
from app.schemas.constants import UserPersonalListType


if TYPE_CHECKING:
    from ... import User
    from . import UserPersonalListItem


class UserPersonalList(Base):
    """
    Таблица описывает персональные списки пользователей для произведений.
    При создании нового пользователя, у него должны быть сгенерированы
    списки по умолчанию, в зависимости от языкового кода:
     + Читаю (Reading)
     + В планах (Plans)
     + Брошено (Dropped)
     + Прочитано (Read)
     + Любимое (Likes)
    """

    __tablename__ = "user_personal_lists"
    __table_args__ = (UniqueConstraint("user_id", "list_name", name="uq_user_personal_list"),)

    # Первичный ключ
    personal_list_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Идентификатор пользовательского списка."
    )

    # Значения
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False,
        comment= "Идентификатор пользователя которому принадлежит этот список."
    )
    list_name: Mapped[str] = mapped_column(
        String(32), nullable=False,
        comment="Название персонального списка."
    )
    list_type: Mapped[UserPersonalListType] = mapped_column(
        nullable=False, comment="Может ли пользователь редактировать этот список"
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), comment="Время обновления пользовательского списка."
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), comment="Время создания пользовательского списка."
    )

    # Связи
    user: Mapped["User"] = relationship(lazy="selectin", back_populates="user_personal_list")
    items: Mapped[List["UserPersonalListItem"]] = relationship(lazy="selectin", back_populates="personal_list")

    def __repr__(self):
        return (f"<UserPersonalList("
                f"personal_list_id = '{self.personal_list_id}',"
                f" user_id = '{self.user_id}', "
                f"list_name = '{self.list_name}', "
                f"list_type = '{self.list_type}')>")
