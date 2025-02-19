from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.utils import settings
from app.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Инициализация базы данных
    yield


def create_app():
    """ Функция для инициализации точки входа """
    app = FastAPI(
        title="Bookworm api server",
        description=
        """
        API-сервер для приложения "Книгочей", написан для дипломной работы, студентом Понкратовым Н. А.
        """,
        version="1.0.0",
        lifespan=lifespan
    )

    from app.api import users
    app.include_router(prefix="/api/v1", router=users.v1_router)
    return app
