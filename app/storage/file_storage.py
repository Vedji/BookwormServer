from abc import ABC, abstractmethod
from fastapi import UploadFile, File, Response
from pydantic import Field

from app.schemas.constants import S3ACL


class FileStorage(ABC):

    @abstractmethod
    async def upload_file(
            self,
            file_key: str = Field(...),
            file: UploadFile = File(...),
            file_acl: S3ACL = S3ACL.PRIVATE
    ) -> Response:
        """
        Абстрактный метод для загрузки файла

        :param file_key: Ключ файла (`{Путь к файлу}/{имя файла}`)
        :param file: Данные файла
        :param file_acl: Права доступа (Только для S3)
        """
        pass

    @abstractmethod
    async def read_file(self, file_key: str) -> Response:
        """
        Абстрактный метод для чтения файла

        :param file_key: Ключ файла (`{Путь к файлу}/{имя файла}`)
        """
        pass

    @abstractmethod
    async def replace_file(self, file_key: str, new_file: UploadFile = File(...)) -> Response:
        """
        Абстрактный метод для замены файла

        :param file_key: Ключ файла (`{Путь к файлу}/{имя файла}`)
        :param new_file: Новый файл для замены
        """
        pass

    @abstractmethod
    async def delete_file(self, file_key: str) -> Response:
        """
        Абстрактный метод для удаления файла
        :param file_key: Ключ файла (`{Путь к файлу}/{имя файла}`)
        """
        pass
