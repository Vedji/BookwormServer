import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

# import app modules
from app.models.reviews import BookComment
from app.schemas.constants import UserRoleDB
from schemas.constants import AllowedBookFileFormats

# import test environment
from .. import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm.books import BookCrudORM
from tests.utils.orm.users import UserCrudORM


class TestBookComments:
    """Тестирует ORM-модель для списка комментариев пользователей для книг. """

    @pytest.mark.asyncio
    async def test_book_comments(self, get_db_local_case: AsyncSession):
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
        book_comment_1 = BookComment(
            user_id=user.user_id,
            book_id=book.book_id,
            message="Test-message-for-comment."
        )
        get_db_local_case.add(book_comment_1)
        book_comment_2 = BookComment(
            user_id=user_2.user_id,
            book_id=book.book_id,
            message="Test-message-for-comment."
        )
        get_db_local_case.add(book_comment_2)
        book_comment_3 = BookComment(
            user_id=user.user_id,
            book_id=book_2.book_id,
            message="Test-message-for-comment."
        )
        get_db_local_case.add(book_comment_3)
        await get_db_local_case.commit()

        await get_db_local_case.refresh(user)
        assert book_comment_1 in user.book_comments and book_comment_3 in user.book_comments
