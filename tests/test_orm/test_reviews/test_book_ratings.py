import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

# import app modules
from app import schemas
from app.models.books import Book, BookPreviewImage
from app.models.reviews import BookRating
from app.schemas.constants import UserRoleDB
from schemas.constants import AllowedBookFileFormats, FileStatus

# import test environment
from .. import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm import FileCrudORM
from tests.utils.orm.books import BookCrudORM
from tests.utils.orm.users import UserCrudORM


class TestBookRatings:
    """Тестирует ORM-модель для списка оценок пользователей для книги. """

    @pytest.mark.asyncio
    async def test_create(self, get_db_local_case: AsyncSession):
        user = await UserCrudORM.create_user(get_db_local_case, username="username", role=UserRoleDB.USER.value)
        user_2 = await UserCrudORM.create_user(get_db_local_case, username="username-2", role=UserRoleDB.USER.value)

        # Создаем и проверяем книгу
        book = await BookCrudORM.create_book(
            get_db_local_case,
            book_publication_date=datetime(1024, 6, 6),
            book_content=None,
            book_content_type=AllowedBookFileFormats.NONE,
            book_isbn="9780733426094",
            added_user=user.user_id
        )
        book_2 = await BookCrudORM.create_book(
            get_db_local_case,
            book_publication_date=datetime(1024, 6, 6),
            book_content=None,
            book_content_type=AllowedBookFileFormats.NONE,
            book_isbn="9780733426093",
            added_user=user.user_id
        )
        await get_db_local_case.commit()

        rating_1 = BookRating(
            user_id=user.user_id,
            book_id=book.book_id,
            rating=4
        )
        get_db_local_case.add(rating_1)

        rating_2 = BookRating(
            user_id=user_2.user_id,
            book_id=book.book_id,
            rating=3
        )
        get_db_local_case.add(rating_2)
        rating_3 = BookRating(
            user_id=user_2.user_id,
            book_id=book_2.book_id,
            rating=3
        )
        get_db_local_case.add(rating_3)

        await get_db_local_case.commit()
        await get_db_local_case.refresh(rating_1)
        await get_db_local_case.refresh(user)
        await get_db_local_case.refresh(user_2)
        await get_db_local_case.refresh(book)

        assert rating_1.rating == 4
        assert rating_1 in user.book_ratings
        assert rating_1 in book.book_ratings and rating_2 in book.book_ratings
        assert rating_3 in user_2.book_ratings and rating_2 in user_2.book_ratings
