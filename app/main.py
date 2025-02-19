from fastapi import FastAPI

from app.utils import settings


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


# Запуск сервера (если выполняем напрямую)
if __name__ == "__main__":
    import uvicorn
    if settings.is_dev:
        uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT, log_level="debug")
    elif settings.is_prod:
        uvicorn.run(app,host=settings.SERVER_HOST, port=settings.SERVER_PORT, log_level="info")
