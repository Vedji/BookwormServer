import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

# import app modules
from app.models import File
from app.models.users import User
from app import schemas, settings

# import test environment
from . import (init_sqlite_db_local_case,  get_db_local_case)


class TestFiles:

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
        new_user = User(username=self.USERNAME, role=self.ROLE)
        get_db_local_case.add(new_user)
        await get_db_local_case.commit()

        assert new_user.user_id is not None, "Пользователь существует?"
        assert new_user.username == self.USERNAME, "Соответствует ли никнейм?"
        assert new_user.role == self.ROLE, "Соответствует ли роль?"

        new_file = File(
            file_key=file_key,
            mime_type=mime_type.value,
            status=status.value,
            bucket_name=bucket_name,
            s3_url=s3_url,
            expires_at=expires_at,
            added_user=new_user.user_id
        )
        get_db_local_case.add(new_file)
        await get_db_local_case.commit()

        file_from_db = await get_db_local_case.get(File, new_file.file_id)

        assert file_from_db.file_key == file_key
        assert file_from_db.mime_type == mime_type.value
        assert file_from_db.status == status.value
        assert file_from_db.bucket_name == bucket_name
        assert file_from_db.s3_url == s3_url
        assert file_from_db.expires_at == expires_at
        assert file_from_db.added_user == new_user.user_id
        assert file_from_db.user == new_user

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
        new_user = User(username=self.USERNAME, role=self.ROLE)
        get_db_local_case.add(new_user)
        await get_db_local_case.commit()

        assert new_user.user_id is not None, "Пользователь существует?"
        assert new_user.username == self.USERNAME, "Соответствует ли никнейм?"
        assert new_user.role == self.ROLE, "Соответствует ли роль?"

        new_file = File(
            file_key=file_key,
            mime_type=mime_type.value,
            status=status.value,
            bucket_name=bucket_name,
            s3_url=s3_url,
            expires_at=expires_at,
            added_user=new_user.user_id
        )
        get_db_local_case.add(new_file)
        await get_db_local_case.commit()

        file_from_db = await get_db_local_case.get(File, new_file.file_id)

        assert file_from_db.file_key == file_key
        assert file_from_db.mime_type == mime_type.value
        assert file_from_db.status == status.value
        assert file_from_db.bucket_name == bucket_name
        assert file_from_db.s3_url == s3_url
        assert file_from_db.expires_at == expires_at
        assert file_from_db.added_user == new_user.user_id
        assert file_from_db.user == new_user

        await get_db_local_case.delete(file_from_db)
        await get_db_local_case.commit()

        deleted = await get_db_local_case.get(File, new_file.file_id)
        assert deleted is None, "Проверяем, удалился ли пользователь?"

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
        new_user = User(username=self.USERNAME, role=self.ROLE)
        get_db_local_case.add(new_user)
        await get_db_local_case.commit()

        assert new_user.user_id is not None, "Пользователь существует?"
        assert new_user.username == self.USERNAME, "Соответствует ли никнейм?"
        assert new_user.role == self.ROLE, "Соответствует ли роль?"

        new_file = File(
            file_key=file_key,
            mime_type=mime_type.value,
            status=status.value,
            bucket_name=bucket_name,
            s3_url=s3_url,
            expires_at=expires_at,
            added_user=new_user.user_id
        )
        get_db_local_case.add(new_file)
        await get_db_local_case.commit()

        file_from_db = await get_db_local_case.get(File, new_file.file_id)

        assert file_from_db.file_key == file_key
        assert file_from_db.mime_type == mime_type.value
        assert file_from_db.status == status.value
        assert file_from_db.bucket_name == bucket_name
        assert file_from_db.s3_url == s3_url
        assert file_from_db.expires_at == expires_at
        assert file_from_db.added_user == new_user.user_id
        assert file_from_db.user == new_user

        file_from_db.status = schemas.constants.FileStatus.DELETED.value
        await get_db_local_case.commit()
        await  get_db_local_case.refresh(file_from_db)

        deleted = await get_db_local_case.get(File, new_file.file_id)
        assert deleted.status == schemas.constants.FileStatus.DELETED.value, "Проверяем, удалился ли пользователь?"


