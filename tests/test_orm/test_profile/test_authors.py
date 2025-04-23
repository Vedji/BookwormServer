import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date

# import app modules
from app.models.users.roles.author import Authors, AuthorCurators, BookAuthors
from app.schemas.constants import UserRoleDB, AllowedBookFileFormats

# import test environment
from .. import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm.books import BookCrudORM
from tests.utils.orm.users import UserCrudORM


class TestAuthors:
    """Тестирует ORM-модель для авторов книг. """

    @pytest.mark.asyncio
    async def test_authors(self, get_db_local_case: AsyncSession):
        user_1 = await UserCrudORM.create_user(get_db_local_case, username="username", role=UserRoleDB.USER.value)
        user_2 = await UserCrudORM.create_user(get_db_local_case, username="username-2", role=UserRoleDB.USER.value)

        # Создаем и проверяем книгу
        book_1 = await BookCrudORM.create_book(
            get_db_local_case,
            book_publication_date=datetime(1024, 6, 6),
            book_content=None,
            book_content_type=AllowedBookFileFormats.FB2,
            book_isbn="9780733426094",
            added_user=user_1.user_id
        )
        book_2 = await BookCrudORM.create_book(
            get_db_local_case,
            book_publication_date=datetime(1024, 6, 6),
            book_content=None,
            book_content_type=AllowedBookFileFormats.EPUB,
            book_isbn="9780733426093",
            added_user=user_2.user_id
        )
        get_db_local_case.add_all([book_1, book_2])
        await get_db_local_case.commit()

        author = Authors(
            first_name="test_first_name",
            last_name="test_last_name",
            contact_email="test@email.ru",
            website="tttt",
            birthday=date(2025,4,23),
            description="what?"
        )
        get_db_local_case.add(author)
        await get_db_local_case.commit()
        author_cur = AuthorCurators(
            account_id=user_1.user_id,
            author_id=author.author_id
        )
        get_db_local_case.add(author_cur)
        await get_db_local_case.commit()

        book_author_1 = BookAuthors(
            author_id=author.author_id,
            book_id=book_1.book_id
        )
        get_db_local_case.add(book_author_1)
        await get_db_local_case.commit()
        await get_db_local_case.refresh(book_1)
        await get_db_local_case.refresh(author)
        await get_db_local_case.refresh(user_1)

        assert book_1.author.author.first_name == "test_first_name"
        assert book_1.book_id in map(lambda x: x.book_id, author.books)
        assert user_1.author_curator.author_id == author.author_id
