from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from app.db import Base

if TYPE_CHECKING:
    from ...user import User
    from . import Authors


class AuthorCurators(Base):
    """
    Таблица хранить курирующие аккаунты для авторов книг.
    """

    __tablename__ = "author_curators"

    author_curator_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Уникальный идентификатор куратора автора.")
    account_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False, comment="Идентификатор курирующего пользователя.")
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.author_id"), nullable=False, comment="Идентификатор автора.")

    user: Mapped["User"] = relationship(
        lazy="selectin", back_populates="author_curator", uselist=False
    )
    author: Mapped["Authors"] = relationship(
        lazy="selectin", back_populates="author_curators", uselist=False
    )

    def __repr__(self):
        return (f"<models.users.roles.publisher.AuthorCurators("
                f"author_curator_id='{self.author_curator_id}', "
                f"account_id='{self.account_id}', "
                f"publisher_id='{self.publisher_id}')>")
