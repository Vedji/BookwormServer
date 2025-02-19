import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

# import app modules
from app.models import User
from app import schemas

# import test environment
from . import (init_sqlite_db_local_case,  get_db_local_case)


class TestUser:

    CREATE_USER_TESTS = [
        ("test_user_user", schemas.constants.UserRoleDB.USER),
        ("test_user_author", schemas.constants.UserRoleDB.AUTHOR),
        ("test_user_publisher", schemas.constants.UserRoleDB.PUBLISHER),
        ("test_user_administrator", schemas.constants.UserRoleDB.ADMINISTRATOR)
    ]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("username, role",CREATE_USER_TESTS)
    async def test_create_user(self, username, role, get_db_local_case: AsyncSession):
        new_user = User(username=username, role=role)
        get_db_local_case.add(new_user)
        await get_db_local_case.commit()

        assert new_user.user_id is not None, "Пользователь существует?"
        assert new_user.username == username, "Соответствует ли никнейм?"
        assert new_user.role == role, "Соответствует ли роль?"

    @pytest.mark.asyncio
    async def test_create_user_unique(self, get_db_local_case: AsyncSession):
        username = "test_user_unique"
        role = schemas.constants.UserRoleDB.USER

        new_user = User(username=username, role=role)
        get_db_local_case.add(new_user)
        await get_db_local_case.commit()

        assert new_user.user_id is not None, "Пользователь существует?"
        assert new_user.username == username, "Соответствует ли никнейм?"
        assert new_user.role == role, "Соответствует ли роль?"

        with pytest.raises(IntegrityError) as integrity_error:
            new_user_2 = User(username=username, role=role)
            get_db_local_case.add(new_user_2)
            await get_db_local_case.commit()

        assert "UNIQUE constraint failed" in integrity_error.value.orig.__str__(),\
            "Проверка, что от БД выброшено исключение об уникальности"


    @pytest.mark.asyncio
    async def test_delete_user(self, get_db_local_case: AsyncSession):
        username = "test_user_unique"
        role = schemas.constants.UserRoleDB.USER

        new_user = User(username=username, role=role)
        get_db_local_case.add(new_user)
        await get_db_local_case.commit()

        assert new_user.user_id is not None, "Пользователь существует?"
        assert new_user.username == username, "Соответствует ли никнейм?"
        assert new_user.role == role, "Соответствует ли роль?"

        user_in_db = await get_db_local_case.get(User, new_user.user_id)
        assert user_in_db == new_user, "Соответствует ли пользователь полученный по ID, созданному ранее?"

        await get_db_local_case.delete(new_user)
        await get_db_local_case.commit()

        user_in_db = await get_db_local_case.get(User, new_user.user_id)
        assert user_in_db is None, "Проверяем, удалился ли пользователь?"
