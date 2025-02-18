from fastapi import APIRouter

v1_router = APIRouter(prefix="/users", tags=["v1/Users"])


@v1_router.get(path="/")
async def v1_get_users():
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

