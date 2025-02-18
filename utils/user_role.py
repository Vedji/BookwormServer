from pydantic import BaseModel
from enum import IntEnum, IntFlag

class UserRole(IntEnum):
    """
    Определяет роли пользователей в системе.

    Возможные роли:

    + 0 - Неавторизованный пользователь.
    + 1 - Авторизованный пользователь.
    + 2 - Автор произведения.
    + 3 - Издатель.
    + 4 - Администратор.
    """

    GUEST = 0  # Неавторизованный пользователь
    USER = 1  # Авторизованный пользователь
    AUTHOR = 2  # Автор произведения
    PUBLISHER = 3  # Издатель
    ADMIN = 4  # Администратор

    @classmethod
    def get_description(cls, value):
        descriptions = {
            UserRole.GUEST: "Неавторизованный пользователь",
            UserRole.USER: "Авторизованный пользователь",
            UserRole.AUTHOR: "Автор произведения",
            UserRole.PUBLISHER: "Издатель",
            UserRole.ADMIN: "Администратор"
        }
        return descriptions.get(value, "Неизвестная роль")
