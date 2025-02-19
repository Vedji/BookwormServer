from fastapi import FastAPI
from app.utils import settings


def create_app():
    """ Функция для инициализации точки входа """
    app = FastAPI(
        title="Bookworm api server",
        description=
        """
        API-сервер для приложения "Книгочей", написан для дипломной работы, студентом Понкратовым Н. А.
        """,
        version="1.0.0"
    )

    from app.api import users
    app.include_router(prefix="/api/v1", router=users.v1_router)
    return app
