# import app modules
from app.utils import settings
from app.storage import S3Storage, LocalStorage, _create_storage_service

# import test fixtures
from tests.conftest import modified_settings


def test_is_set_local_storage(monkeypatch, modified_settings):
    """
    Тестирует приватную функцию _create_storage_service,
    при USE_S3 = False, (должно создаться локальное хранилище)
    """

    monkeypatch.setattr(settings, "USE_S3", False)
    files_storage = _create_storage_service()
    assert isinstance(files_storage, LocalStorage), f"LocalStorage == {files_storage.__class__}"


def test_is_set_s3_storage(monkeypatch, modified_settings):
    """
    Тестирует приватную функцию _create_storage_service,
    при USE_S3 = True, (должно создаться S3-хранилище)
    """

    monkeypatch.setattr(settings, "USE_S3", True)
    files_storage = _create_storage_service()
    assert isinstance(files_storage, S3Storage), f"S3Storage == {files_storage.__class__}"
