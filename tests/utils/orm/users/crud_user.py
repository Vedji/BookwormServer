from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User, UserDetails, UserCredentials


class UserCrudORM:
    """
    Класс объединяющей Crud операции над ORM-моделями из модуля `app.models.users`
    """

    @staticmethod
    async def create_user_details(db: AsyncSession, **kwargs) -> UserDetails:
        """
        Создает и проверяет запись о детальной информации пользователя.
        Обязательно соответствие kwargs полям класса UserDetails

        :param db: Сессия базы данных.
        :param kwargs: Поля класса UserDetails для заполнения.
        """
        user_details = UserDetails(**kwargs)
        db.add(user_details)
        await db.commit()

        for key, value in kwargs.items():
            assert getattr(user_details, key) == value, \
                f"In models.UserDetails {key} assert -> ' {getattr(user_details, key)} != {value}'"

        return user_details

    @staticmethod
    async def create_user_credentials(db: AsyncSession, **kwargs) -> UserCredentials:
        """
        Создает и проверяет запись о данных для аутентификации пользователя.
        Обязательно соответствие kwargs полям класса UserCredentials

        :param db: Сессия базы данных.
        :param kwargs: Поля класса UserCredentials для заполнения.
        """
        user_credentials = UserCredentials(**kwargs)
        db.add(user_credentials)
        await db.commit()

        for key, value in kwargs.items():
            assert getattr(user_credentials,
                           key) == value, f"In models.UserCredentials {key} assert -> ' {getattr(user_credentials, key)} != {value}'"

        return user_credentials

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
