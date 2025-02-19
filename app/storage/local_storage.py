import shutil
from pathlib import Path
from fastapi import UploadFile, File, HTTPException, Response

# import app modules files
from app.schemas.constants import S3ACL

# import local module files
from .file_storage import FileStorage


class LocalStorage(FileStorage):
    """Класс для работы с локальным хранилищем файлов."""

    def __init__(self, storage_dir: str):
        """
        Инициализация локального хранилища
        :param storage_dir: Директория хранения файлов
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    async def upload_file(self, file_key: str, file: UploadFile = File(...), file_acl: S3ACL = S3ACL.PRIVATE) -> Response:
        """
        Загрузка файла в локальное хранилище
        :param file_key: Ключ файла (`{Путь к файлу}/{имя файла}`)
        :param file: Данные файла
        :param file_acl: Права доступа **Unused**
        """

        file_path = self.storage_dir / file_key
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return Response(status_code=201)

    async def read_file(self, file_key: str) -> Response:
        """
        Чтение файла из локального хранилища
        :param file_key: Ключ файла (`{Путь к файлу}/{имя файла}`)
        """

        file_path = self.storage_dir / file_key
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Файл не найден")
        with file_path.open("rb") as f:
            file_content = f.read()
        return Response(content=file_content, media_type="application/octet-stream", status_code=200)

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

    async def delete_file(self, file_key: str) -> Response:
        """
        Удаление файла из локального хранилища
        :param file_key: Ключ файла (`{Путь к файлу}/{имя файла}`)
        """

        file_path = self.storage_dir / file_key
        if file_path.exists():
            file_path.unlink()
            return Response(status_code=204)
        raise HTTPException(status_code=404, detail="Файл не найден")

