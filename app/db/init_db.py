from sqlalchemy import (String, ForeignKey, UniqueConstraint, event, insert)
from app.db.session import engine

from app.schemas.constants import LanguageCodes

from app.db.base import Base
from app.models import *


async def init_db():
    """Создаёт таблицы в базе данных при первом запуске."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@event.listens_for(Language.__table__, 'after_create')
def insert_initial_data(target, connection, **kw):
    """Создание языков по умолчанию, при создании таблицы `languages` для ORM-модели `Language`. """
    connection.execute(
        insert(Language),
        [
            {"language_code": LanguageCodes.RU.value, "language_name": "Русский"},
            {"language_code": LanguageCodes.EN.value, "language_name": "Английский"},
        ]
    )
