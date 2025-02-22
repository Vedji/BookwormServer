from sqlalchemy.ext.asyncio import AsyncSession

from app.models.books import Book


class BookCrudORM:
    """
    Класс объединяющей Crud операции над ORM-моделями из модуля ```app.models.books.Book```.
    """

    @staticmethod
    async def create_book(db: AsyncSession, **kwargs) -> Book:
        """
        Создает и проверяет запись о файле. Обязательно соответствие kwargs полям класса Book

        :param db: Сессия базы данных.
        :param kwargs: Поля класса Book для заполнения.
        """
        book = Book(**kwargs)
        db.add(book)
        await db.commit()

        for key, value in kwargs.items():
            assert getattr(book, key) == value, f"In models.File {key} assert -> ' {getattr(book, key)} != {value}'"

        return book
