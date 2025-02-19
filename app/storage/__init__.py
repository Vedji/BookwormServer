"""
Модуль отвечает за работу с файловой системой, в зависимости от значения USE_S3 в settings,
работа с файлами будет производиться либо в s3-совместимом хранилищем(`USE_S3=True`),
либо в локальном хранилище(`USE_S3=False`)

Необходимые файлы окружения из settings:

Для S3:
 - S3_URL
 - S3_BUCKET_NAME
 - S3_ACCESS_KEY
 - S3_SECRET_ACCESS_KEY
 - S3_REGION
 - S3_PROJECT_PREFIX

Для локального хранилища:
 - LOCAL_STORAGE_PATH

Example:

    >>> from app.storage import files_storage
    >>> from app.schemas.constants import S3ACL
    >>> from fastapi import UploadFile
    >>> from io import BytesIO
    >>>
    >>> async def func():
    >>>     file_key = 'folder_example/example.txt'
    >>>     file = UploadFile(filename='example.txt', file=BytesIO(b'Your test file content'))
    >>>     file_acl = S3ACL.PRIVATE
    >>>     response = await files_storage.upload_file(file_key, file, file_acl)
"""

# import local module files
from .s3_storage import S3Storage
from .file_storage import FileStorage
from .local_storage import LocalStorage

# import application module files
from app.utils import settings
from app.utils.config import Settings


def _create_storage_service(sett: Settings = settings) -> FileStorage:
    """ Создает модуль FileStorage в зависимости от выбранного типа хранилища. """
    _storage = None
    if sett.USE_S3:
        _storage = S3Storage(
            bucket_name=sett.S3_BUCKET_NAME,
            s3_url=sett.S3_URL,
            s3_project_prefix=sett.S3_PROJECT_PREFIX,
            aws_access_key_id=sett.S3_ACCESS_KEY,
            aws_secret_access_key=sett.S3_SECRET_ACCESS_KEY,
            region_name=sett.S3_REGION
        )
    else:
        _storage = LocalStorage(sett.LOCAL_STORAGE_PATH)
    return _storage


files_storage: FileStorage = _create_storage_service(settings)
