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
    from .profile.personal_lists import UserPersonalList
    from .profile.bookmarks import UserBookmark
    from ..supports import SupportRequest


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
    # Данные для авторизации пользователя
    credentials: Mapped["UserCredentials"] = relationship(
        lazy="selectin", back_populates="user", uselist=False,
        cascade="all, delete-orphan")
    # Список файлов, которые добавил пользователь
    files: Mapped[List["File"]] = relationship(
        lazy="selectin", back_populates='user',
        cascade="save-update, merge")
    # Детальное описание профиля пользователя
    details: Mapped["UserDetails"] = relationship(
        lazy="selectin", back_populates="user",
        uselist=False, cascade="all, delete-orphan")
    # Список добавленных книг пользователя
    added_books: Mapped[List["Book"]] = relationship(
        lazy="selectin", back_populates="user",
        cascade="save-update, merge")
    # Список оставленных оценок к книгам пользователя
    book_ratings: Mapped[List["BookRating"]] = relationship(
        lazy="selectin", back_populates="user")
    # Список комментариев пользователя к книгам
    book_comments: Mapped[List["BookComment"]] = relationship(
        lazy="selectin", back_populates="user")
    # Список персональных списков пользователя
    user_personal_list: Mapped[List["UserPersonalList"]] = relationship(
        lazy="selectin", back_populates="user")
    # Список закладок пользователя
    user_bookmarks: Mapped[List["UserBookmark"]] = relationship(
        lazy="selectin", back_populates="user")
    # Список отправленных пользователем заявок в техническую поддержку
    submitted_tickets: Mapped[List["SupportRequest"]] = relationship(
        "SupportRequest", lazy="selectin", foreign_keys="SupportRequest.user_id", back_populates="created_by")
    # Список обработанных пользователем заявок из технической поддержки
    reviewed_tickets: Mapped[List["SupportRequest"]] = relationship(
        "SupportRequest", lazy="selectin", foreign_keys="SupportRequest.reviewed_user_id", back_populates="reviewed_by")

    # TODO: Add relationships to:
    #  - author_curators
    #  - publisher_curators

    def __repr__(self):
        return (f"<models.User("
                f"user_id='{self.user_id}',"
                f" username='{self.username}',"
                f" role='{self.role}',"
                f" created_at='{self.created_at}'"
                f")>")
