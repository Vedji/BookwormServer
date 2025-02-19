import uvicorn

from app.utils import settings
from app import create_app


# Запуск сервера (если выполняем напрямую)
if __name__ == "__main__":
    app = create_app()

    if settings.is_dev:
        uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT, log_level="debug")
    elif settings.is_prod:
        uvicorn.run(app,host=settings.SERVER_HOST, port=settings.SERVER_PORT, log_level="info")
