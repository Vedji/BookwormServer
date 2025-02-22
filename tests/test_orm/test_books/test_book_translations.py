import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

# import app modules
from app.schemas.constants import AllowedBookFileFormats, FileStatus, UserRoleDB, LanguageCodes
from app.models import Language

from app.models.books import Book, BookPreviewImage, BookTranslation


# import test environment
from .. import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm import FileCrudORM
from tests.utils.orm.books import BookCrudORM
from tests.utils.orm.users import UserCrudORM


class TestBookTranslation:
    """Тестирует ORM-модель для списка локализации книги. """

    @pytest.mark.asyncio
    async def test_create_book_translations(self, get_db_local_case: AsyncSession):
        user = await UserCrudORM.create_user(get_db_local_case, username="username", role=UserRoleDB.USER.value)

        # Создаем и проверяем книгу
        book = await BookCrudORM.create_book(
            get_db_local_case,
            book_publication_date=datetime(1024, 6, 6),
            book_content=None,
            book_content_type=AllowedBookFileFormats.NONE,
            book_isbn="9780733426094",
            added_user=user.user_id
        )
        await get_db_local_case.commit()

        rus_lang = await get_db_local_case.get(Language, LanguageCodes.RU)
        book_translate = BookTranslation.create(book_id=book.book_id, language_code=LanguageCodes(rus_lang.language_code), book_title="test-title")

        get_db_local_case.add(book_translate)
        await get_db_local_case.commit()
        await get_db_local_case.refresh(book)

        get_translate_from_db = await get_db_local_case.get(BookTranslation, (book.book_id, LanguageCodes.RU))
        assert get_translate_from_db in book.book_translations
        assert book.book_translations[-1].book_title == "test-title"



