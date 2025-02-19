from app.db.session import engine
from app.db.base import Base

async def init_db():
    """Создаёт таблицы в базе данных при первом запуске."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
