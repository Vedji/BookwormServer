import pytest_asyncio
from botocore.config import Config
from _pytest.monkeypatch import MonkeyPatch

from app.utils import settings

S3_TEST_FOLDER = "bookworm-server-test/"


@pytest_asyncio.fixture(scope="session")
def modified_settings():
    monkeypatch = MonkeyPatch()
    monkeypatch.setattr(settings, "S3_PROJECT_PREFIX", S3_TEST_FOLDER)
    yield
    monkeypatch.undo()