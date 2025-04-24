import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

import schemas.constants
# import app modules
from app.models.books.genres import Genre, GenreTranslation, BookGenre
from app.models.books import Book
from app.schemas.constants import UserRoleDB
from schemas.constants import AllowedBookFileFormats, FileStatus

# import test environment
from ... import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm import FileCrudORM
from tests.utils.orm.books import BookCrudORM
from tests.utils.orm.users import UserCrudORM


class TestBookGenres:

    @pytest.mark.asyncio
    async def test_create_book(self, get_db_local_case: AsyncSession):
        username = "test-username"
        role = UserRoleDB.USER.value

        # Создаем пользователя, который будет добавлять книгу
        user = await UserCrudORM.create_user(get_db_local_case, username=username, role=role)
        await get_db_local_case.commit()

        # Создаем и проверяем книгу
        book = await BookCrudORM.create_book(
            get_db_local_case,
            book_publication_date=datetime(1024, 6, 6),
            book_content = None,
            book_content_type=AllowedBookFileFormats.NONE,
            book_isbn="9780733426094",
            added_user=user.user_id
        )
        await get_db_local_case.commit()

        new_genre = Genre()
        get_db_local_case.add(new_genre)
        await get_db_local_case.commit()

        genre_translate = GenreTranslation(
            genre_id=new_genre.genre_id,
            language_code=schemas.constants.LanguageCodes.RU,
            genre_name="Test-genre"
        )
        get_db_local_case.add(genre_translate)
        await get_db_local_case.commit()

        book_genre = BookGenre(book_id=book.book_id, genre_id=new_genre.genre_id)
        get_db_local_case.add(book_genre)
        await get_db_local_case.commit()

        await get_db_local_case.refresh(book)
        await get_db_local_case.refresh(genre_translate)
        await get_db_local_case.refresh(book.book_genres[0].genre)

        await get_db_local_case.commit()
        await get_db_local_case.refresh(book)
        assert book_genre in book.book_genres
        assert book.book_genres[0].genre.genre_translations[0].genre_name == "Test-genre"
