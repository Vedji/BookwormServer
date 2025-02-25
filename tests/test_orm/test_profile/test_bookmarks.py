import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

# import app modules
from app.models.reviews import BookComment
from app.models.users.profile.bookmarks import UserBookmark, BookmarkEPUB, BookmarkFB2
from app.schemas.constants import UserRoleDB, AllowedBookFileFormats

# import test environment
from .. import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm.books import BookCrudORM
from tests.utils.orm.users import UserCrudORM
from app.models.users.profile.personal_lists import UserPersonalList, UserPersonalListItem


class TestUserBookmark:
    """Тестирует ORM-модель для персональных закладок пользователей, для разных форматов книг. """

    @pytest.mark.asyncio
    async def test_user_bookmark(self, get_db_local_case: AsyncSession):
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

        bookmark_11 = UserBookmark(
            user_id=user_1.user_id,
            book_id=book_1.book_id,
            book_file_type=AllowedBookFileFormats.FB2
        )
        bookmark_12 = UserBookmark(
            user_id=user_1.user_id,
            book_id=book_2.book_id,
            book_file_type=AllowedBookFileFormats.EPUB
        )
        bookmark_21 = UserBookmark(
            user_id=user_2.user_id,
            book_id=book_1.book_id,
            book_file_type=AllowedBookFileFormats.FB2
        )
        bookmark_22 = UserBookmark(
            user_id=user_2.user_id,
            book_id=book_2.book_id,
            book_file_type=AllowedBookFileFormats.EPUB
        )
        get_db_local_case.add_all([bookmark_11, bookmark_12, bookmark_21, bookmark_22])
        await get_db_local_case.commit()
        assert bookmark_11.bookmark == 0

        bookmark_fb2_1 = BookmarkFB2(
            bookmark_id=bookmark_11.bookmark_id,
            position=21
        )
        bookmark_fb2_2 = BookmarkFB2(
            bookmark_id=bookmark_21.bookmark_id,
            position=31
        )
        bookmark_epub_1 = BookmarkEPUB(
            bookmark_id=bookmark_12.bookmark_id,
            location="21"
        )
        bookmark_epub_2 = BookmarkEPUB(
            bookmark_id=bookmark_22.bookmark_id,
            location="31"
        )
        get_db_local_case.add_all([bookmark_fb2_1, bookmark_fb2_2, bookmark_epub_1, bookmark_epub_2])
        await get_db_local_case.commit()
        await get_db_local_case.refresh(bookmark_11)
        await get_db_local_case.refresh(bookmark_12)
        await get_db_local_case.refresh(bookmark_21)
        await get_db_local_case.refresh(bookmark_22)

        assert bookmark_fb2_1 is bookmark_11.bookmark_fb2
        assert bookmark_fb2_1.position == 21
        assert bookmark_11.bookmark_epub is None
        assert bookmark_fb2_2 is bookmark_21.bookmark_fb2
        assert bookmark_fb2_2.position == 31
        assert bookmark_21.bookmark_epub is None

        assert bookmark_epub_1 is bookmark_12.bookmark_epub
        assert bookmark_epub_1.location == "21"
        assert bookmark_12.bookmark_fb2 is None
        assert bookmark_epub_2 is bookmark_22.bookmark_epub
        assert bookmark_epub_2.location == "31"
        assert bookmark_22.bookmark_fb2 is None

        buffer_bookmark_id_1 = bookmark_11.bookmark_id
        await get_db_local_case.delete(bookmark_11)
        buffer_bookmark_id_2 = bookmark_12.bookmark_id
        await get_db_local_case.delete(bookmark_12)
        await get_db_local_case.commit()

        bookmark_11 = await get_db_local_case.get(UserBookmark, buffer_bookmark_id_1)
        assert bookmark_11 is None
        bookmark_12 = await get_db_local_case.get(UserBookmark, buffer_bookmark_id_2)
        assert bookmark_12 is None
