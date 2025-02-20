import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

# import app modules
from app.models.users import User, UserCredentials
from app import schemas

# import test environment
from . import (init_sqlite_db_local_case,  get_db_local_case)


class TestUser:

    CREATE_USER_TESTS = [
        (
            "test_user_user", schemas.constants.UserRoleDB.USER,
            "test@email.com", "some_password", schemas.constants.PasswordEncryptionTypes.NONE
        ),
        (
            "test_user_author", schemas.constants.UserRoleDB.AUTHOR,
            "test_2@email.com", "some_password", schemas.constants.PasswordEncryptionTypes.NONE
         ),
        (
            "test_user_publisher", schemas.constants.UserRoleDB.PUBLISHER,
            "test_3@email.com", "some_password", schemas.constants.PasswordEncryptionTypes.NONE
         ),
        (
            "test_user_administrator", schemas.constants.UserRoleDB.ADMINISTRATOR,
            "test_4@email.com", "some_password", schemas.constants.PasswordEncryptionTypes.NONE
        )
    ]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("username, role, email, password_hash, password_encryption", CREATE_USER_TESTS)
    async def test_create_user(
            self,
            username,
            role,
            email,
            password_hash,
            password_encryption,
            get_db_local_case: AsyncSession
    ):
        new_user = User(username=username, role=role)
        get_db_local_case.add(new_user)
        await get_db_local_case.commit()

        assert new_user.user_id is not None, "Пользователь существует?"
        assert new_user.username == username, "Соответствует ли никнейм?"
        assert new_user.role == role, "Соответствует ли роль?"

        new_user_credentials = UserCredentials(
            user_id=new_user.user_id,
            email=email,
            password_hash=password_hash,
            password_encryption=password_encryption.value
        )
        get_db_local_case.add(new_user_credentials)
        await get_db_local_case.commit()
        await get_db_local_case.refresh(new_user_credentials)
        await get_db_local_case.refresh(new_user)

        assert new_user.credentials == new_user_credentials, "Проверка relationship"
        assert new_user.credentials.user_id == new_user.user_id
        assert new_user.credentials.email == email
        assert new_user.credentials.password_hash == password_hash
        assert new_user.credentials.password_encryption == password_encryption

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

    @pytest.mark.asyncio
    async def test_create_user_two_credentials(self, get_db_local_case: AsyncSession):
        username = self.CREATE_USER_TESTS[0][0]
        role = self.CREATE_USER_TESTS[0][1].value
        email = self.CREATE_USER_TESTS[0][2]
        password_hash = self.CREATE_USER_TESTS[0][3]
        password_encryption = self.CREATE_USER_TESTS[0][4].value

        new_user = User(username=username, role=role)
        get_db_local_case.add(new_user)
        await get_db_local_case.commit()

        assert new_user.user_id is not None, "Пользователь существует?"
        assert new_user.username == username, "Соответствует ли никнейм?"
        assert new_user.role == role, "Соответствует ли роль?"

        new_user_credentials = UserCredentials(
            user_id=new_user.user_id,
            email=email,
            password_hash=password_hash,
            password_encryption=password_encryption
        )
        get_db_local_case.add(new_user_credentials)
        await get_db_local_case.commit()
        await get_db_local_case.refresh(new_user_credentials)
        await get_db_local_case.refresh(new_user)

        assert new_user.credentials == new_user_credentials,\
            "Проверка, что у пользователя есть запись об его аутентификационных данных"

        new_user_credentials_2 = UserCredentials(
            user_id=new_user.user_id,
            email=email,
            password_hash=password_hash,
            password_encryption=password_encryption
        )
        with pytest.raises(IntegrityError) as err:
            get_db_local_case.add(new_user_credentials_2)
            await get_db_local_case.commit()

        assert "user_credentials.user_id" in err.value.__str__() and "UNIQUE" in err.value.__str__(), \
            "Ошибка при добавлении второй записи аутентификации для одного пользователя"
