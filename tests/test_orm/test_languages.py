import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

# import app modules
from app import models
from app import schemas

# import test environment
from . import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm import FileCrudORM
from tests.utils.orm.users import UserCrudORM


class TestLanguages:
    """Проверка таблицы языков"""

    @pytest.mark.asyncio
    async def test_languages(self, get_db_local_case: AsyncSession):
        rus_lang = await get_db_local_case.get(models.Language, schemas.constants.LanguageCodes.RU)
        eng_lang = await get_db_local_case.get(models.Language, schemas.constants.LanguageCodes.EN)
        assert rus_lang.language_code == schemas.constants.LanguageCodes.RU
        assert eng_lang.language_code == schemas.constants.LanguageCodes.EN
