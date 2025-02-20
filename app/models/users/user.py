from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import TYPE_CHECKING

from app.db import Base
from app.schemas.constants import UserRoleDB

if TYPE_CHECKING:
    from . import UserCredentials


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Идентификатор пользователя в системе."
    )
    username: Mapped[str] = mapped_column(
        String(128), unique=True, nullable=False,
        comment="Никнейм пользователя."
    )
    role: Mapped[UserRoleDB] = mapped_column(
        default=UserRoleDB.USER, nullable=False,
        comment="Роль авторизированного пользователя. От просто авторизированного, до администратора."
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(), nullable=False,
        comment="Время регистрации пользователя."
    )

    credentials: Mapped["UserCredentials"] = relationship(
        "UserCredentials", back_populates="user", uselist=False, cascade="all, delete-orphan")

    files = relationship('File', back_populates='user', cascade="save-update, merge")

    # TODO: Add relationships to:
    #  - user_details
    #  - support_request
    #  - user_personal_list
    #  - book_rating
    #  - user_bookmark
    #  - books
    #  - author_curators
    #  - publisher_curators

    def __repr__(self):
        return (f"<models.User("
                f"user_id='{self.user_id}',"
                f" username='{self.username}',"
                f" role='{self.role}',"
                f" created_at='{self.created_at}'"
                f")>")
