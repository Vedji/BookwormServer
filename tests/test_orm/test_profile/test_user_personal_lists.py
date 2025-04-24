import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

# import app modules
from app.models.reviews import BookComment
from app.schemas.constants import UserRoleDB, UserPersonalListType
from schemas.constants import AllowedBookFileFormats

# import test environment
from .. import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm.books import BookCrudORM
from tests.utils.orm.users import UserCrudORM
from app.models.users.profile.personal_lists import UserPersonalList, UserPersonalListItem


class TestUserPersonalList:
    """Тестирует ORM-модель для персонального списка пользователей для книг. """

    @pytest.mark.asyncio
    async def test_user_personal_lists(self, get_db_local_case: AsyncSession):
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

        # Создаем персональные списки
        user_1_list = UserPersonalList(
            user_id=user.user_id,
            list_name="test-1",
            list_type=UserPersonalListType.DEFAULT
        )
        user_1_list_2 = UserPersonalList(
            user_id=user.user_id,
            list_name="test-2",
            list_type=UserPersonalListType.DEFAULT
        )
        user_2_list = UserPersonalList(
            user_id=user_2.user_id,
            list_name="test-1",
            list_type=UserPersonalListType.DEFAULT
        )

        get_db_local_case.add_all([user_1_list, user_2_list, user_1_list_2])
        await get_db_local_case.commit()

        # Добавляем книги в пользовательские книги
        list_item_11 = UserPersonalListItem(
            personal_list_id=user_1_list.personal_list_id,
            book_id=book.book_id
        )
        list_item_12 = UserPersonalListItem(
            personal_list_id=user_1_list.personal_list_id,
            book_id=book_2.book_id
        )
        list_item_21 = UserPersonalListItem(
            personal_list_id=user_2_list.personal_list_id,
            book_id=book.book_id
        )
        list_item_22 = UserPersonalListItem(
            personal_list_id=user_2_list.personal_list_id,
            book_id=book_2.book_id
        )
        get_db_local_case.add_all([list_item_11, list_item_12, list_item_21, list_item_22])
        await get_db_local_case.commit()

        # Проверяем пользовательские списки
        await get_db_local_case.refresh(user)
        await get_db_local_case.refresh(user_2)
        await get_db_local_case.refresh(user.user_personal_list[0])

        assert user_1_list in user.user_personal_list
        assert list_item_11 in user.user_personal_list[0].items and list_item_11 in user.user_personal_list[0].items
