from enum import Enum


class SupportRequestTypes(str, Enum):
    """
    Перечисление доступных типов заявок от пользователей.
        - 'REQUEST_TYPE_NONE' - тип тикета не указан(none-тип),
        - 'REQUEST_ABOUT_ERROR' - тикет сообщения об ошибки,
        - 'REQUEST_TO_GET_AUTHOR_ROLE' - тикет с заявкой на получение аккаунта автора контента,
        - 'REQUEST_TO_GET_PUBLISHER_ROLE' - тикет с заявкой на получение аккаунта издательства,
        - 'REQUEST_TO_GET_ADMINISTRATOR_ROLE' - тикет с заявкой на получение аккаунта администратора.
    """

    REQUEST_TYPE_NONE = "request_type_none"
    REQUEST_ABOUT_ERROR = "request_about_error"
    REQUEST_TO_GET_AUTHOR_ROLE = "request_to_get_author_role"
    REQUEST_TO_GET_PUBLISHER_ROLE = "request_to_get_publisher_role"
    REQUEST_TO_GET_ADMINISTRATOR_ROLE = "request_to_get_administrator_role"
