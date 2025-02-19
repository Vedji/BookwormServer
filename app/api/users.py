from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import Users
from app.db import get_db

v1_router = APIRouter(prefix="/users", tags=["v1/Users"])


@v1_router.get(path="/")
async def v1_get_users(db: AsyncSession  = Depends(get_db)):
    await Users.get(db)
    return {"message": "Получить пользователей"}


@v1_router.post(path="/")
async def v1_create_user():
    return {"message": "Создать нового пользователя"}


@v1_router.patch(path="/")
async def v1_edit_user():
    return {"message": "Изменить пользователя"}


@v1_router.delete(path="/")
async def v1_delete_user():
    return {"message": "Удалить пользователя"}

