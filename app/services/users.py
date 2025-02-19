from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User


class Users:

    @staticmethod
    async def get(db: AsyncSession):
        result = await db.execute(select(User))
        users = result.scalars().all()  # Извлекаем объекты
        print(users)
