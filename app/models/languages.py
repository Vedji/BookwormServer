from sqlalchemy import (String, ForeignKey, UniqueConstraint, event, insert)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List, TYPE_CHECKING
import datetime

from app.db import Base
from app.schemas.constants import AllowedFileFormats, FileStatus, LanguageCodes


class Language(Base):
    __tablename__ = "languages"

    language_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False,
        comment="Идентификатор языка в БД.")
    language_code: Mapped["LanguageCodes"] = mapped_column(
        nullable=False, unique=True,
        comment="Языковой код ('en', 'ru' и т.п.)")
    language_name: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="Название языка"
    )

    # TODO: Add relationships for:
    #   - genres_translations
    #   - book_translations
    #   - book_comments

