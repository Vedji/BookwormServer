from enum import Enum


class UserRoleDB(str, Enum):
    user = "USER"                               # Просто авторизированный пользователь
    author = "AUTHOR"                           # Автор книг
    publisher = "PUBLISHER"                     # Издатель книг
    administrator = "ADMINISTRATOR"             # Администратор


class UserRole(str, Enum):
    GUEST = "GUEST"                             # Гость
    user = UserRoleDB.user                      # Просто авторизированный пользователь
    author = UserRoleDB.author                  # Автор книг
    publisher = UserRoleDB.publisher            # Издатель книг
    administrator = UserRoleDB.administrator    # Администратор
