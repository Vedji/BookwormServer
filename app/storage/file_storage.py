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
        """Метод для загрузки файла"""
        pass

    @abstractmethod
    async def read_file(self, file_key: str) -> Response:
        """Метод для получения файла"""
        pass

    @abstractmethod
    async def replace_file(self, file_key: str, new_file: UploadFile = File(...)) -> Response:
        """Метод для замены файла"""
        pass

    @abstractmethod
    async def delete_file(self, file_key: str) -> Response:
        """ Метод для удаления файла"""
        pass
