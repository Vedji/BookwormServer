
# Пример использования
import asyncio
from io import BytesIO

from fastapi import UploadFile

from app import settings
from app.storage.file_storage import FileStorage
from app.storage.s3_storage import S3Storage

async def main():
    # Вывод списка файлов
    test_file_key = "test_file.txt"
    test_file_content = b"Hello, S3!"
    update_test_file_content = b"Hello, S3!"

    new_s3_storage: FileStorage = S3Storage(
        bucket_name=settings.S3_BUCKET_NAME,
        s3_url=settings.S3_URL,
        s3_project_prefix=settings.S3_PROJECT_PREFIX,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION
    )
    new_file = UploadFile(filename=test_file_key, file=BytesIO(test_file_content))
    print()
    response = await new_s3_storage.upload_file(file_key=test_file_key, file=new_file)
    print("Загрузка файла: ", response)
    print("Чтение файла: ", (await new_s3_storage.read_file(file_key=test_file_key)))
    print()
    new_file = UploadFile(filename=test_file_key, file=BytesIO(update_test_file_content))
    print("Замена файла: ", await new_s3_storage.replace_file(test_file_key, new_file))
    print("Чтение замененного файла: ", await new_s3_storage.read_file(test_file_key))
    print()
    print("Удаление файла: ", await new_s3_storage.delete_file(test_file_key))
    print("Чтение удаленного файла: ", await new_s3_storage.read_file(test_file_key))
    print()

if __name__ == "__main__":
    asyncio.run(main())