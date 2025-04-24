import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date

# import app modules
from app.models.users.roles.publisher import Publishers, PublisherCurators, BookPublishers
from app.schemas.constants import UserRoleDB, AllowedBookFileFormats

# import test environment
from .. import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm.books import BookCrudORM
from tests.utils.orm.users import UserCrudORM


class TestPublishers:
    """Тестирует ORM-модель для издателей книг. """

    @pytest.mark.asyncio
    async def test_publishers(self, get_db_local_case: AsyncSession):
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

        pub = Publishers(
            publisher_name="test",
            website="tttt",
            contact_email="test@email.ru",
            contact_phone="+7000000",
            founded_year=date(2025,4,23),
            description="what?"
        )
        get_db_local_case.add(pub)
        await get_db_local_case.commit()
        pub_cur = PublisherCurators(
            account_id=user_1.user_id,
            publisher_id=pub.publisher_id
        )
        get_db_local_case.add(pub_cur)
        await get_db_local_case.commit()

        book_pub_1 = BookPublishers(
            publisher_id=pub.publisher_id,
            book_id=book_1.book_id
        )
        get_db_local_case.add(book_pub_1)
        await get_db_local_case.commit()
        await get_db_local_case.refresh(book_1)
        await get_db_local_case.refresh(pub)
        await get_db_local_case.refresh(user_1)

        assert book_1.publisher.publisher.publisher_name == "test"
        assert book_1.book_id in map(lambda x: x.book_id, pub.books)
        assert user_1.publisher_curator.publisher_id == pub.publisher_id
