from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING, List
from datetime import datetime
from app.db import Base

if TYPE_CHECKING:
    from .. import Book
    from ...users import User
    from . import BookForumAnswers


class BookForumQuestions(Base):
    """
    Таблица хранит вопросы к книгам (в формате вопрос-ответы).
    """

    __tablename__ = "book_forum_questions"

    forum_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Идентификатор форума.")
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id"), nullable=False, comment="Идентификатор книги, к которой относится вопрос."
    )
    is_open: Mapped[bool] = mapped_column(
        nullable=False, default=True, comment="Открыто ли обсуждение?"
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False, comment="Заголовок вопроса.")
    question_message: Mapped[str] = mapped_column(nullable=True, comment="Текст вопроса.")

    added_user: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False, comment="Пользователь, который добавил этот вопрос.")
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), comment="Время создания вопроса."
    )

    user: Mapped["User"] = relationship(lazy="selectin", back_populates="book_forum_questions", uselist=False)
    book: Mapped["Book"] = relationship(lazy="selectin", back_populates="book_forum_questions", uselist=False)
    answers: Mapped[List["BookForumAnswers"]] = relationship(lazy="selectin", back_populates="question")

    def __repr__(self):
        return (f"models.books.forums.BookForumQuestions<("
                f"forum_id='{self.forum_id}', book_id='{self.book_id}', title='{self.title}')>")
