from sqlalchemy import (String, ForeignKey, UniqueConstraint)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import TYPE_CHECKING
import datetime

from app.db import Base
from app.schemas.constants import AllowedFileFormats, FileStatus

if TYPE_CHECKING:
    from .users import User


class File(Base):
    __tablename__ = "files"

    file_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Идентификатор файла в БД."
    )

    file_key: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False,
        comment="Ключ файла в формате S3 (`{file_path}/{file_name}`)."
    )
    mime_type: Mapped[AllowedFileFormats] = mapped_column(
        default=AllowedFileFormats.INCORRECT_FILE_FORMAT, nullable=False,
        comment="Mime-тип файла."
    )

    status: Mapped[FileStatus] = mapped_column(
        default=FileStatus.ACTIVE, nullable=True,
        comment="Статус файла (Можно получить по S3 ссылке, хранится в локальном хранилище и т.п.)"
    )
    bucket_name: Mapped[str] = mapped_column(
        String(64), nullable=True, comment="Имя бакета S3.")
    s3_url: Mapped[str] = mapped_column(
        String(512), nullable=True, comment="Прямая ссылка на файл в S3.")
    expires_at: Mapped[datetime.datetime] = mapped_column(
        nullable=True,
        comment="Время окончания действия ссылки."
    )
    uploaded_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(), nullable=False,
        comment="Время загрузки файла на сервер."
    )
    added_user: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True,
        comment="Id пользователя, добавившего файл."
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="files", uselist=False)
    user_details = relationship(
        "UserDetails", back_populates="profile_image")

    # TODO: Add relationships to:
    #  - Books (ref: < book_content, ref: < book_title_image)

    __table_args__ = (
        UniqueConstraint('file_key', name='uq_file_key'),
    )

    def __repr__(self):
        return f"<FileDto(file_id='{self.file_id}', status='{self.status}', file_key='{self.file_key}')>"
