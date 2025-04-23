import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

# import app modules
from app.models.users import User, UserCredentials, UserDetails, UserLoginAttempts
from app import schemas

# import test environment
from tests.utils.orm import FileCrudORM
from tests.utils.orm.users import UserCrudORM
from . import (init_sqlite_db_local_case,  get_db_local_case)




class TestUser:
    """
    Тестирование ORM-моделей из модуля app.models.users

    Тестируется следующие ORM-классы из этого модуля:
        - User
        - UserCredentials
        - UserDetails
        - UserLoginAttempts
    """

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
    async def test_user_details(self, get_db_local_case: AsyncSession):
        """ Проверяет ORM класс для таблицы `user_details` """

        username = "test_user_unique"
        role = schemas.constants.UserRoleDB.USER

        # Создание нового пользователя и его проверка
        user = await UserCrudORM.create_user(get_db_local_case, username=username, role=role)

        # Создание записи в таблице user_details
        user_details = await UserCrudORM.create_user_details(
            get_db_local_case,
            user_id=user.user_id,
            description=None,
            profile_image_id=None
        )

        # Проверяем соответствие внешних ключей
        await get_db_local_case.refresh(user)
        assert user.details == user_details

        # Создаем файл и добавляем его, как аватарку пользователя
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
        user_details.profile_image = file
        await get_db_local_case.commit()
        await get_db_local_case.refresh(user_details)
        await get_db_local_case.refresh(file)

        # Проверяем что файл корректно установился
        assert user_details.profile_image == file
        assert user_details.profile_image_id == file.file_id

        # Удаляем аватарку пользователя
        await get_db_local_case.delete(file)
        await get_db_local_case.commit()
        await get_db_local_case.refresh(user_details)

        # Проверяем что у пользователя установилось значение null у аватарки пользователя
        assert user_details.profile_image is None
        assert user_details.profile_image_id is None

        # Добавление второго пользователя с такими же данными
        with pytest.raises(IntegrityError) as integrity_error:
            await UserCrudORM.create_user_details(
                get_db_local_case,
                user_id=user.user_id,
                description=None,
                profile_image_id=None
            )

        # Проверка, что SQLAlchemy выдало исключение об уникальности
        assert "UNIQUE constraint failed" in integrity_error.value.orig.__str__(), \
            "Проверка, что от БД выброшено исключение об уникальности"
        assert "user_details.user_id" in integrity_error.value.__str__(),\
            "Проверка, что от БД выброшено исключение об уникальности"

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
        new_user = await UserCrudORM.create_user(get_db_local_case, username=username, role=role)

        # Добавление к пользователю данных для аутентификации и их проверка
        new_user_credentials = await UserCrudORM.create_user_credentials(
            get_db_local_case,
            user_id=new_user.user_id,
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
        await UserCrudORM.create_user(get_db_local_case, username=username, role=role)

        # Добавление второго пользователя с такими же данными
        with pytest.raises(IntegrityError) as integrity_error:
            await UserCrudORM.create_user(get_db_local_case, username=username, role=role)

        # Проверка, что SQLAlchemy выдало исключение об уникальности
        assert "UNIQUE constraint failed" in integrity_error.value.orig.__str__(),\
            "Проверка, что от БД выброшено исключение об уникальности"

    @pytest.mark.asyncio
    async def test_delete_user(self, get_db_local_case: AsyncSession):
        username = "test_user_unique"
        role = schemas.constants.UserRoleDB.USER

        # Создание нового пользователя и его проверка
        new_user = await UserCrudORM.create_user(get_db_local_case, username=username, role=role)

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
        new_user = await UserCrudORM.create_user(get_db_local_case, username=username, role=role)

        # Создаем запись для аутентификации пользователя.
        new_user_credentials = await UserCrudORM.create_user_credentials(
            get_db_local_case,
            user_id=new_user.user_id,
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
            await UserCrudORM.create_user_credentials(
                get_db_local_case,
                user_id=new_user.user_id,
                email=email,
                password_hash=password_hash,
                password_encryption=password_encryption
            )

        # Проверяем, что SQLAlchemy выбросило исключение об уникальности записей в таблице аутентификации пользователей.
        assert "user_credentials.user_id" in err.value.__str__() and "UNIQUE" in err.value.__str__(), \
            "Ошибка при добавлении второй записи аутентификации для одного пользователя"

    @pytest.mark.asyncio
    async def test_user_login_attempts(self, get_db_local_case: AsyncSession):
        """ Проверяет ORM класс для таблицы `user_login_attempts` """
        role = schemas.constants.UserRoleDB.USER

        # Создание нового пользователя и его проверка
        user = await UserCrudORM.create_user(get_db_local_case, username="username-1", role=role)

        ula_1 = UserLoginAttempts(
            user_id=user.user_id,
            is_success=False,
            ip_address="192.168.0.1"
        )
        ula_2 = UserLoginAttempts(
            user_id=user.user_id,
            is_success=True,
            ip_address="192.168.0.2"
        )
        get_db_local_case.add_all([ula_1, ula_2])
        await get_db_local_case.commit()
        await get_db_local_case.refresh(user)

        assert ula_1 in user.user_login_attempt
        assert ula_2 in user.user_login_attempt

        assert list(filter(lambda x: x.ip_address == "192.168.0.2", user.user_login_attempt))[0].is_success
        assert not list(filter(lambda x: x.ip_address == "192.168.0.1", user.user_login_attempt))[0].is_success
