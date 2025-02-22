import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

# import app modules
from app.models import File
from app.models.users import User
from app import schemas

# import test environment
from . import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm import FileCrudORM
from tests.utils.orm.users import UserCrudORM


class TestFiles:
    """
    Тестирование ORM-модели файлов, класс:`app.modules.File`.
    """

    USERNAME = "test-username"
    ROLE = schemas.constants.UserRoleDB.ADMINISTRATOR

    test_cases_files = [
        ("file1.pdf", schemas.constants.AllowedFileFormats.PDF, schemas.constants.FileStatus.ACTIVE, "documents",
         "https://s3.timeweb.cloud/documents/file1.pdf", datetime.now() + timedelta(days=30)),
        ("readme.md", schemas.constants.AllowedFileFormats.MARKDOWN, schemas.constants.FileStatus.EXPIRED, "markdown-files",
         "https://s3.timeweb.cloud/markdown-files/readme.md", datetime.now() - timedelta(days=5)),
        ("backup.zip", schemas.constants.AllowedFileFormats.ZIP, schemas.constants.FileStatus.DELETED, "backups",
         "https://s3.timeweb.cloud/backups/backup.zip", datetime.now() + timedelta(days=90)),
        ("image.png", schemas.constants.AllowedFileFormats.PNG, schemas.constants.FileStatus.LOCAL, "images", "image.png", None),
        ("photo.jpeg", schemas.constants.AllowedFileFormats.JPEG, schemas.constants.FileStatus.ACTIVE, "photos",
         "https://s3.timeweb.cloud/photos/photo.jpeg", datetime.now() + timedelta(days=7)),
        ("animation.gif", schemas.constants.AllowedFileFormats.GIF, schemas.constants.FileStatus.ACTIVE, "animations",
         "https://s3.timeweb.cloud/animations/animation.gif", datetime.now() - timedelta(days=1)),
        ("notes.txt", schemas.constants.AllowedFileFormats.TXT, schemas.constants.FileStatus.ACTIVE, "text-files",
         "https://s3.timeweb.cloud/text-files/notes.txt", datetime.now() + timedelta(days=365)),
        ("null_case_file.txt", schemas.constants.AllowedFileFormats.TXT,
         schemas.constants.FileStatus.ACTIVE, None, None, None)
    ]


    @pytest.mark.asyncio
    @pytest.mark.parametrize("file_key, mime_type, status, bucket_name, s3_url, expires_at", test_cases_files)
    async def test_create_file(
            self,
            file_key: str,
            mime_type: schemas.constants.AllowedFileFormats,
            status: schemas.constants.FileStatus,
            bucket_name: str,
            s3_url: str,
            expires_at: datetime,
            get_db_local_case: AsyncSession
    ):
        # Создание пользователя, который добавляет файл
        new_user = await UserCrudORM.create_user(get_db_local_case, username=self.USERNAME, role=self.ROLE)

        # Создание записи о файле в БД
        new_file = await FileCrudORM.create_file(
            get_db_local_case,
            file_key=file_key,
            mime_type=mime_type.value,
            status=status.value,
            bucket_name=bucket_name,
            s3_url=s3_url,
            expires_at=expires_at,
            added_user=new_user.user_id
        )

        # Проверка существования и соответствия записи о файле с ожидаемыми значениями
        file_from_db = await get_db_local_case.get(File, new_file.file_id)
        assert file_from_db.file_key == file_key
        assert file_from_db.mime_type == mime_type.value
        assert file_from_db.status == status.value
        assert file_from_db.bucket_name == bucket_name
        assert file_from_db.s3_url == s3_url
        assert file_from_db.expires_at == expires_at
        assert file_from_db.added_user == new_user.user_id
        assert file_from_db.user == new_user

        # Удаление пользователя
        await get_db_local_case.delete(new_user)
        await get_db_local_case.commit()
        await get_db_local_case.refresh(file_from_db)
        new_user = await get_db_local_case.get(User, new_user.user_id)

        # Проверка, что пользователь удален и файл остался
        assert new_user is None
        assert file_from_db.user is None
        assert file_from_db.file_key == file_key


    @pytest.mark.asyncio
    @pytest.mark.parametrize("file_key, mime_type, status, bucket_name, s3_url, expires_at", test_cases_files)
    async def test_hard_delete_file(
            self,
            file_key: str,
            mime_type: schemas.constants.AllowedFileFormats,
            status: schemas.constants.FileStatus,
            bucket_name: str,
            s3_url: str,
            expires_at: datetime,
            get_db_local_case: AsyncSession
    ):
        # Создание пользователя, который добавляет файл.
        new_user = await UserCrudORM.create_user(get_db_local_case, username=self.USERNAME, role=self.ROLE)

        # Создание новой записи о файле в БД.
        new_file = await FileCrudORM.create_file(
            get_db_local_case,
            file_key=file_key,
            mime_type=mime_type.value,
            status=status.value,
            bucket_name=bucket_name,
            s3_url=s3_url,
            expires_at=expires_at,
            added_user=new_user.user_id
        )

        # Удаление файла
        await get_db_local_case.delete(new_file)
        await get_db_local_case.commit()

        # Проверка удаления файла
        deleted = await get_db_local_case.get(File, new_file.file_id)
        assert deleted is None, "Проверяем, удалился ли файл?"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("file_key, mime_type, status, bucket_name, s3_url, expires_at", test_cases_files)
    async def test_soft_delete_file(
            self,
            file_key: str,
            mime_type: schemas.constants.AllowedFileFormats,
            status: schemas.constants.FileStatus,
            bucket_name: str,
            s3_url: str,
            expires_at: datetime,
            get_db_local_case: AsyncSession
    ):
        # Создание пользователя, который добавляет файл.
        new_user = await UserCrudORM.create_user(get_db_local_case, username=self.USERNAME, role=self.ROLE)

        # Создание новой записи о файле в БД.
        new_file = await FileCrudORM.create_file(
            get_db_local_case,
            file_key=file_key,
            mime_type=mime_type.value,
            status=status.value,
            bucket_name=bucket_name,
            s3_url=s3_url,
            expires_at=expires_at,
            added_user=new_user.user_id
        )

        # Мягкое удаление файла (Помечаем его в БД, как удаленный)
        new_file.status = schemas.constants.FileStatus.DELETED.value
        await get_db_local_case.commit()
        await  get_db_local_case.refresh(new_file)

        # Проверяем, что у файла в БД изменился статус на удаленный
        deleted = await get_db_local_case.get(File, new_file.file_id)
        assert deleted.status == schemas.constants.FileStatus.DELETED.value, "Проверяем, удалился ли файл?"


