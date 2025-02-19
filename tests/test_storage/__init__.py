import pytest_asyncio, boto3
from botocore.config import Config
from app.utils import settings

from app.storage import S3Storage
from tests import modified_settings



@pytest_asyncio.fixture(scope="module")
def s3_storage(modified_settings) -> S3Storage:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION,
        endpoint_url=settings.S3_URL,
        config=Config(signature_version='s3v4')
    )
    bucket_name = settings.S3_BUCKET_NAME
    folder_name = settings.S3_PROJECT_PREFIX

    # Находим все объекты с этим префиксом
    objects_to_delete = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)

    if "Contents" in objects_to_delete:
        delete_keys = [{"Key": obj["Key"]} for obj in objects_to_delete["Contents"]]

        # Удаляем все объекты
        s3.delete_objects(Bucket=bucket_name, Delete={"Objects": delete_keys})
        print(f'Папка "{folder_name}" удалена из {bucket_name}')
    else:
        print(f'Папка "{folder_name}" уже пустая или не существует.')

    storage = S3Storage(
        bucket_name=settings.S3_BUCKET_NAME,
        s3_url=settings.S3_URL,
        s3_project_prefix=settings.S3_PROJECT_PREFIX,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION
    )
    return storage