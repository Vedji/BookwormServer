import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

# import app modules
from app.models.books import Book
from app.schemas.constants import UserRoleDB
from schemas.constants import AllowedBookFileFormats, FileStatus

# import test environment
from .. import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm import FileCrudORM
from tests.utils.orm.books import BookCrudORM
from tests.utils.orm.users import UserCrudORM


class TestBook:

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

        # Создаем файл и добавляем его к книге
        file = await FileCrudORM.create_file(
            get_db_local_case,
            file_key="file_key",
            mime_type=AllowedBookFileFormats.FB2.value,
            status=FileStatus.LOCAL.value,
            bucket_name="bucket_name",
            s3_url="s3_url",
            expires_at=datetime.now() + timedelta(days=30),
            added_user=user.user_id
        )
        await get_db_local_case.commit()
        book.content = file
        book.book_content_type = AllowedBookFileFormats.FB2
        await get_db_local_case.commit()
        await get_db_local_case.refresh(book)
        assert book.content == file
        assert book.book_content_type == AllowedBookFileFormats.FB2.value

        # Удаляем файл книги и проверяем, что книга осталась
        await get_db_local_case.delete(file)
        book.book_content_type = AllowedBookFileFormats.NONE.value
        await get_db_local_case.commit()
        await get_db_local_case.refresh(book)

        assert book.content is None
        assert book.book_content is None
        assert book.book_content_type == AllowedBookFileFormats.NONE.value
        # Удаляем книгу и проверяем, что пользователь остался
        await get_db_local_case.delete(book)
        await get_db_local_case.commit()
        await get_db_local_case.refresh(user)

        assert user is not None
