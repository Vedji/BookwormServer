from fastapi import UploadFile, File, Response, HTTPException
import aioboto3
from botocore.config import Config
from pydantic import Field

from app.utils import errors
from app.schemas.constants import S3ACL

from .file_storage import FileStorage


class S3Storage(FileStorage):
    """Класс для работы с S3 совместимым хранилищем. """

    def __init__(
            self,
            bucket_name: str,
            s3_url: str,
            s3_project_prefix: str = "",
            aws_access_key_id: str=None,
            aws_secret_access_key: str=None,
            region_name: str='ru-1'
    ):
        """
        Инициализация асинхронного S3 клиента
        :param bucket_name: Название S3-бакета
        :param aws_access_key_id: (опционально) Access Key ID
        :param aws_secret_access_key: (опционально) Secret Access Key
        :param region_name: (опционально) Регион AWS
        """

        self.bucket_name = bucket_name
        self.session = aioboto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.s3_url = s3_url
        self.s3_project_prefix = s3_project_prefix
        self.s3_config = Config(signature_version='s3')


    @errors.handle_s3_errors
    async def upload_file(
            self,
            file_key: str = Field(...),
            file: UploadFile = File(...),
            file_acl: S3ACL = S3ACL.PRIVATE
    ) -> Response:
        """
        Загрузка файла в S3-хранилище
        :param file_key: Ключ файла (`{Путь к файлу}/{имя файла}`)
        :param file: Данные файла
        :param file_acl: Права доступа
        """

        file_key = f"{self.s3_project_prefix}{file_key}"
        content_type = file.content_type if file.content_type else "application/octet-stream"
        extra_args = {
            'ACL': file_acl.value,                  # Права доступа
            'ContentType': content_type,            # MIME-тип
        }
        async with self.session.client('s3', endpoint_url=self.s3_url, config=self.s3_config) as s3:
            await s3.upload_fileobj(file.file, self.bucket_name, file_key, ExtraArgs=extra_args)
        return Response(status_code=201)

    @errors.handle_s3_errors
    async def read_file(self, file_key: str) -> Response:
        """
        Чтение файла из S3-хранилища
        :param file_key: Ключ файла (`{Путь к файлу}/{имя файла}`)
        """

        file_key = f"{self.s3_project_prefix}{file_key}"
        async with self.session.client('s3', endpoint_url=self.s3_url, config=self.s3_config) as s3:
            response = await s3.get_object(Bucket=self.bucket_name, Key=file_key)
            file_content = await response['Body'].read()
            content_type = response.get('ContentType', 'application/octet-stream')
            return Response(content=file_content, media_type=content_type, status_code=200)

    @errors.handle_s3_errors
    async def replace_file(self, file_key: str, new_file: UploadFile = File(...)) -> Response:
        """
        Замена файла в локальном хранилище

        :param file_key: Ключ файла (`{Путь к файлу}/{имя файла}`)
        :param new_file: Новый файл для замены
        """

        deleted = await self.delete_file(file_key)
        if not deleted:
            raise HTTPException(status_code=500, detail=f"Ошибка: не удалось удалить файл {file_key}")
        await self.upload_file(file_key, new_file)
        return Response(status_code=204)

    @errors.handle_s3_errors
    async def delete_file(self, file_key: str) -> Response:
        """
        Удаление файла из S3-хранилища

        :param file_key: Ключ файла (`{Путь к файлу}/{имя файла}`)
        """

        file_key = f"{self.s3_project_prefix}{file_key}"
        async with self.session.client('s3', endpoint_url=self.s3_url, config=self.s3_config) as s3:
            await s3.delete_object(Bucket=self.bucket_name, Key=file_key)
            return Response(status_code=204)
