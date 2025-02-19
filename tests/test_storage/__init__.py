import pytest_asyncio, boto3, shutil
from botocore.config import Config

from app.utils import settings
from app.storage import S3Storage, LocalStorage

from tests import modified_settings


@pytest_asyncio.fixture(scope="module")
def local_storage(modified_settings) -> LocalStorage:
    storage = LocalStorage(settings.LOCAL_STORAGE_PATH)
    yield storage

    # Очистка после завершения тестов
    try:
        if storage.storage_dir.exists():
            shutil.rmtree(storage.storage_dir)  # Удаляем всю директорию хранения
    except Exception as e:
        print(f"Ошибка при очистке локального хранилища: {e}")


@pytest_asyncio.fixture(scope="module")
def s3_storage(modified_settings) -> S3Storage:
    s3_storage_clear(
        aws_access_key_id = settings.S3_ACCESS_KEY,
        aws_secret_access_key = settings.S3_SECRET_ACCESS_KEY,
        region_name = settings.S3_REGION,
        endpoint_url = settings.S3_URL,
        bucket_name=settings.S3_BUCKET_NAME,
        folder_name = settings.S3_PROJECT_PREFIX
    )

    storage = S3Storage(
        bucket_name=settings.S3_BUCKET_NAME,
        s3_url=settings.S3_URL,
        s3_project_prefix=settings.S3_PROJECT_PREFIX,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION
    )
    yield storage

    # Очистка после завершения тестов
    try:
        s3_storage_clear(
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
            region_name=settings.S3_REGION,
            endpoint_url=settings.S3_URL,
            bucket_name=settings.S3_BUCKET_NAME,
            folder_name=settings.S3_PROJECT_PREFIX
        )
    except Exception as e:
        print(f"Ошибка при очистке S3-хранилища: {e}")


def s3_storage_clear(
        aws_access_key_id,
        aws_secret_access_key,
        region_name,
        endpoint_url,
        bucket_name,
        folder_name
):
    """ Очистка и удаление директории в S3-хранилище для тестирования. """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        endpoint_url=endpoint_url,
        config=Config(signature_version='s3v4')
    )

    # Находим все объекты с этим префиксом
    objects_to_delete = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)

    if "Contents" in objects_to_delete:
        delete_keys = [{"Key": obj["Key"]} for obj in objects_to_delete["Contents"]]

        # Удаляем все объекты
        s3.delete_objects(Bucket=bucket_name, Delete={"Objects": delete_keys})
        print(f'Папка "{folder_name}" удалена из {bucket_name}')
    else:
        print(f'Папка "{folder_name}" уже пустая или не существует.')
