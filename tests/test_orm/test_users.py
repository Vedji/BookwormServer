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

    @staticmethod
    async def create_user(db: AsyncSession, **kwargs) -> User:
        """
        Создает и проверяет запись о пользователе. Обязательно соответствие kwargs полям класса User

        :param db: Сессия базы данных.
        :param kwargs: Поля класса User для заполнения.
        """
        user = User(**kwargs)
        db.add(user)
        await db.commit()

        for key, value in kwargs.items():
            assert getattr(user, key) == value, f"In models.User {key} assert -> ' {getattr(user, key)} != {value}'"

        return user

    @staticmethod
    async def create_user_credentials(db: AsyncSession, user: User, **kwargs) -> UserCredentials:
        """
        Создает и проверяет запись о данных для аутентификации пользователя.
        Обязательно соответствие kwargs полям класса UserCredentials

        :param db: Сессия базы данных.
        :param user: Пользователь к которому эти записи относятся.
        :param kwargs: Поля класса UserCredentials для заполнения.
        """
        user_credentials = UserCredentials(user_id=user.user_id, **kwargs)
        db.add(user_credentials)
        await db.commit()

        for key, value in kwargs.items():
            assert getattr(user_credentials, key) == value, f"In models.UserCredentials {key} assert -> ' {getattr(user_credentials, key)} != {value}'"

        return user_credentials

    @pytest.mark.asyncio
    @pytest.mark.parametrize("username, role, email, password_hash, password_encryption", CREATE_USER_TESTS)
    async def test_create_user(
            self,
            username: str,
            role: schemas.constants.UserRoleDB,
            email: str,
            password_hash: str,
            password_encryption: schemas.constants.PasswordEncryptionTypes,
            get_db_local_case: AsyncSession
    ):
        # Создание нового пользователя и его проверка
        new_user = await self.create_user(get_db_local_case, username=username, role=role)

        # Добавление к пользователю данных для аутентификации и их проверка
        new_user_credentials = await self.create_user_credentials(
            get_db_local_case,
            new_user,
            email=email,
            password_hash=password_hash,
            password_encryption=password_encryption.value
        )
        await get_db_local_case.refresh(new_user)

        # Проверка, что данные можно корректно получить через внешний ключ
        assert new_user.credentials == new_user_credentials, "Проверка relationship"
        assert new_user.credentials.user_id == new_user.user_id
        assert new_user.credentials.email == email
        assert new_user.credentials.password_hash == password_hash
        assert new_user.credentials.password_encryption == password_encryption

    @pytest.mark.asyncio
    async def test_create_user_unique(self, get_db_local_case: AsyncSession):
        username = "test_user_unique"
        role = schemas.constants.UserRoleDB.USER

        # Создание нового пользователя и его проверка
        await self.create_user(get_db_local_case, username=username, role=role)

        # Добавление второго пользователя с такими же данными
        with pytest.raises(IntegrityError) as integrity_error:
            await self.create_user(get_db_local_case, username=username, role=role)

        # Проверка, что SQLAlchemy выдало исключение об уникальности
        assert "UNIQUE constraint failed" in integrity_error.value.orig.__str__(),\
            "Проверка, что от БД выброшено исключение об уникальности"

    @pytest.mark.asyncio
    async def test_delete_user(self, get_db_local_case: AsyncSession):
        username = "test_user_unique"
        role = schemas.constants.UserRoleDB.USER

        # Создание нового пользователя и его проверка
        new_user = await self.create_user(get_db_local_case, username=username, role=role)

        # Получаем пользователя из БД и проверяем его.
        user_in_db = await get_db_local_case.get(User, new_user.user_id)
        assert user_in_db == new_user, "Соответствует ли пользователь полученный по ID, созданному ранее?"

        # Удаляем пользователя из БД
        await get_db_local_case.delete(new_user)
        await get_db_local_case.commit()

        # Проверяем, что пользователь удалился
        user_in_db = await get_db_local_case.get(User, new_user.user_id)
        assert user_in_db is None, "Проверяем, удалился ли пользователь?"

    @pytest.mark.asyncio
    async def test_create_user_two_credentials(self, get_db_local_case: AsyncSession):
        username = self.CREATE_USER_TESTS[0][0]
        role = self.CREATE_USER_TESTS[0][1].value
        email = self.CREATE_USER_TESTS[0][2]
        password_hash = self.CREATE_USER_TESTS[0][3]
        password_encryption = self.CREATE_USER_TESTS[0][4].value

        # Создаем пользователя в БД
        new_user = await self.create_user(get_db_local_case, username=username, role=role)

        # Создаем запись для аутентификации пользователя.
        new_user_credentials = await self.create_user_credentials(
            get_db_local_case,
            new_user,
            email=email,
            password_hash=password_hash,
            password_encryption=password_encryption
        )

        # Проверяем, что ORM корректно отображает зависимость между ними
        await get_db_local_case.refresh(new_user)
        assert new_user.credentials == new_user_credentials,\
            "Проверка, что у пользователя есть запись об его аутентификационных данных"

        # Добавляем вторую запись о данных для аутентификации пользователя
        with pytest.raises(IntegrityError) as err:
            await self.create_user_credentials(
                get_db_local_case,
                new_user,
                email=email,
                password_hash=password_hash,
                password_encryption=password_encryption
            )

        # Проверяем, что SQLAlchemy выбросило исключение об уникальности записей в таблице аутентификации пользователей.
        assert "user_credentials.user_id" in err.value.__str__() and "UNIQUE" in err.value.__str__(), \
            "Ошибка при добавлении второй записи аутентификации для одного пользователя"
