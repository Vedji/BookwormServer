import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

# import app modules
from app import schemas
from app.models.books import Book, BookPreviewImage
from app.schemas.constants import UserRoleDB
from schemas.constants import AllowedBookFileFormats, FileStatus

# import test environment
from .. import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm import FileCrudORM
from tests.utils.orm.books import BookCrudORM
from tests.utils.orm.users import UserCrudORM


class TestBookPreviewImage:
    """Тестирует ORM-модель для списка превью-изображений для книги. """

    @pytest.mark.asyncio
    async def test_create(self, get_db_local_case: AsyncSession):
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

        file = await FileCrudORM.create_file(
            get_db_local_case,
            file_key="file_key",
            mime_type=schemas.constants.AllowedFileFormats.JPEG.value,
            status=schemas.constants.FileStatus.EXPIRED.value,
            bucket_name=None,
            s3_url=None,
            expires_at=None,
            added_user=user.user_id
        )
        file_2 = await FileCrudORM.create_file(
            get_db_local_case,
            file_key="file_key_2",
            mime_type=schemas.constants.AllowedFileFormats.JPEG.value,
            status=schemas.constants.FileStatus.EXPIRED.value,
            bucket_name=None,
            s3_url=None,
            expires_at=None,
            added_user=user.user_id
        )

        assert file.file_id != file_2.file_id

        bpe = BookPreviewImage.create(
            book_id=book.book_id, file_id=file.file_id, content_description="Some description!")
        get_db_local_case.add(bpe)
        bpe_2 = BookPreviewImage.create(
            book_id=book.book_id, file_id=file_2.file_id, content_description="Some description 2!")
        get_db_local_case.add(bpe_2)

        await get_db_local_case.commit()
        await get_db_local_case.refresh(user)
        await get_db_local_case.refresh(book)
        await get_db_local_case.refresh(file)

        assert bpe in book.preview_images
        assert bpe_2 in book.preview_images




