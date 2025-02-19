from abc import ABC, abstractmethod
from fastapi import UploadFile, File


class FileStorage(ABC):

    @abstractmethod
    def upload_file(self, file: UploadFile = File(...)):
        """Метод для загрузки файла"""
        pass

    @abstractmethod
    def read_file(self, file_key: str) -> bytes:
        """Метод для получения файла"""
        pass

    @abstractmethod
    def replace_file(self, file_key: str, new_file: UploadFile = File(...)):
        """Метод для замены файла"""
        pass

    @abstractmethod
    def delete_file(self, file_key: str):
        """ Метод для удаления файла"""
        pass
