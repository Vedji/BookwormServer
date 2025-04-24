from enum import Enum


class UserRoleDB(str, Enum):
    USER = "USER"                               # Просто авторизированный пользователь
    AUTHOR = "AUTHOR"                           # Автор книг
    PUBLISHER = "PUBLISHER"                     # Издатель книг
    ADMINISTRATOR = "ADMINISTRATOR"             # Администратор


class UserRole(str, Enum):
    GUEST = "GUEST"                             # Гость
    USER = UserRoleDB.USER                      # Просто авторизированный пользователь
    AUTHOR = UserRoleDB.AUTHOR                  # Автор книг
    PUBLISHER = UserRoleDB.PUBLISHER            # Издатель книг
    ADMINISTRATOR = UserRoleDB.ADMINISTRATOR    # Администратор
