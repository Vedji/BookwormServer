from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from datetime import datetime
from app.db import Base

if TYPE_CHECKING:
    from ...users import User
    from . import BookForumQuestions


class BookForumAnswers(Base):
    """
    Таблица ответов к вопросам для форума (главный вопрос - ответы).
    """

    __tablename__ = "book_forum_answers"

    answer_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Идентификатор ответа.")
    forum_id: Mapped[int] = mapped_column(
        ForeignKey("book_forum_questions.forum_id"),
        nullable=False, comment="Идентификатор вопроса, к которому относится этот ответ.")
    message: Mapped[str] = mapped_column(
        nullable=False, comment="Сообщение ответа.")
    added_user: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False, comment="Пользователь, который оставил этот ответ.")
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), comment="Время, когда был оставлен этот ответ.")

    question: Mapped["BookForumQuestions"] = relationship(lazy="selectin", back_populates="answers", uselist=False)
    user: Mapped["User"] = relationship(lazy="selectin", back_populates="", uselist=False)

    def __repr__(self):
        return (f"models.books.forums.BookForumAnswers<("
                f"answer_id='{self.answer_id}', forum_id='{self.forum_id}', added_user='{self.added_user}')>")
