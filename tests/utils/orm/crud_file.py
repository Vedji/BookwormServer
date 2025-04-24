from sqlalchemy.ext.asyncio import AsyncSession

from app.models import File


class FileCrudORM:
    """
    Класс объединяющей Crud операции над ORM-моделями из модуля `app.models.File`.
    """

    @staticmethod
    async def create_file(db: AsyncSession, **kwargs) -> File:
        """
        Создает и проверяет запись о файле. Обязательно соответствие kwargs полям класса File

        :param db: Сессия базы данных.
        :param kwargs: Поля класса File для заполнения.
        """
        file = File(**kwargs)
        db.add(file)
        await db.commit()

        for key, value in kwargs.items():
            assert getattr(file, key) == value, f"In models.File {key} assert -> ' {getattr(file, key)} != {value}'"

        return file