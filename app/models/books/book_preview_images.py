from sqlalchemy import String, ForeignKey, Date, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
import datetime

from app.db import Base

if TYPE_CHECKING:
    from .. import File
    from . import Book


class BookPreviewImage(Base):
    __tablename__ = "book_preview_images"

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id"), primary_key=True, nullable=False,
        comment="Идентификатор книги.")
    file_id: Mapped[int] =mapped_column(
        ForeignKey("files.file_id"), primary_key=True, nullable=False,
        comment="Идентификатор изображения."
    )

    content_description: Mapped[str] = mapped_column(
        String(128), nullable=True, default="Описание изображения отсутствует.",
        comment="Описание изображения.")
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default=func.now(),
        comment="Когда книга была записана в систему."
    )

    # Связи
    for_book: Mapped["Book"] = relationship(lazy="selectin", back_populates="preview_images", uselist=False)
    preview_content: Mapped["File"] = relationship(lazy="selectin", back_populates="book_preview_image_list", uselist=False)

    @staticmethod
    def create(
            book_id: int,
            file_id: int,
            content_description: str = None,
            created_at: datetime.datetime = None
    ) -> "BookPreviewImage":
        """Создает новый объект типа `BookPreviewImage` и возвращает его. """
        new = BookPreviewImage(book_id=book_id, file_id=file_id)
        if content_description:
            new.content_description = content_description
        if created_at:
            new.created_at = created_at
        return new



    def __repr__(self):
        return f"<BookPreviewImage(book_id = '{self.book_id}', file_id='{self.file_id}')>"

