import functools

from fastapi import HTTPException
from botocore.exceptions import NoCredentialsError, ClientError, EndpointConnectionError



def handle_s3_errors(func):
    """Декоратор для обработки ошибок S3-хранилища."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except NoCredentialsError as e:
            raise HTTPException(
                status_code=401,
                detail=f"{NoCredentialsError.__class__}: отсутствуют учетные данные для S3."
            )

        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            error_code_mapping = {
                "NoSuchBucket": 404,                # Бакет не найден
                "NoSuchKey": 404,                   # Файл не найден
                "AccessDenied": 403,                # Нет доступа
                "InvalidArgument": 400,             # Неправильные аргументы
                "InvalidBucketName": 400,           # Некорректное имя бакета
                "RequestTimeout": 408,              # Тайм-аут запроса
                "ThrottlingException": 429,         # Лимит запросов превышен
                "InternalError": 500,               # Внутренняя ошибка S3
                "ServiceUnavailable": 503,          # S3 недоступен
            }

            error_message_mapping = {
                "NoSuchBucket": "Бакет не найден",                  # Бакет не найден
                "NoSuchKey": "Файл не найден",                      # Файл не найден
                "AccessDenied": "Нет доступа",                      # Нет доступа
                "InvalidArgument": "Неправильные аргументы",        # Ошибочные аргументы
                "InvalidBucketName": "Некорректное имя бакета",     # Некорректное имя бакета
                "RequestTimeout": "Время доступа превышено",        # Тайм-аут запроса
                "ThrottlingException": "Достигнут лимит запросов",  # Лимит запросов превышен
                "InternalError": "Внутренняя ошибка S3",            # Внутренняя ошибка S3
                "ServiceUnavailable": "S3 недоступен",              # S3 недоступен
            }

            status_code = error_code_mapping.get(error_code, 500)
            error_message = error_message_mapping.get(error_code, "Unknown error")

            raise HTTPException(status_code=status_code, detail=error_message)

        except EndpointConnectionError as e:
            raise HTTPException(status_code=503, detail="Проблемы с подключением к S3")

        except HTTPException as e:
            raise e

    return wrapper