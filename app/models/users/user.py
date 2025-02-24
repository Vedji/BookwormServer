from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List, TYPE_CHECKING

from app.db import Base
from app.schemas.constants import UserRoleDB

if TYPE_CHECKING:
    from . import UserCredentials, UserDetails
    from .. import File
    from ..books import Book
    from ..reviews import BookRating, BookComment



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

    # Связи
    credentials: Mapped["UserCredentials"] = relationship(
        lazy="selectin", back_populates="user", uselist=False, cascade="all, delete-orphan")
    files: Mapped[List["File"]] = relationship(
        lazy="selectin", back_populates='user', cascade="save-update, merge")
    details: Mapped["UserDetails"] = relationship(
        lazy="selectin", back_populates="user", uselist=False, cascade="all, delete-orphan")
    added_books: Mapped[List["Book"]] = relationship(
        lazy="selectin", back_populates="user", cascade="save-update, merge")
    book_ratings: Mapped[List["BookRating"]] = relationship(
        lazy="selectin", back_populates="user")
    book_comments: Mapped[List["BookComment"]] = relationship(
        lazy="selectin"
    )

    # TODO: Add relationships to:
    #  - support_request
    #  - user_personal_list
    #  - user_bookmark
    #  - author_curators
    #  - publisher_curators

    def __repr__(self):
        return (f"<models.User("
                f"user_id='{self.user_id}',"
                f" username='{self.username}',"
                f" role='{self.role}',"
                f" created_at='{self.created_at}'"
                f")>")
