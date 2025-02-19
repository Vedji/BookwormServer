from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from app.utils import settings


DATABASE_URL = (f"mysql+aiomysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}"
     f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DBNAME}")

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, )


async def get_db():
    """Функция для получения сессии БД (зависимость для FastAPI)."""
    async with AsyncSessionLocal() as session:
        yield session
