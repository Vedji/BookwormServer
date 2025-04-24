import pytest_asyncio
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

import app.db.session
from app.db.base import Base


@pytest_asyncio.fixture(scope="function")
async def init_sqlite_db_local_case():
    app.db.session.DATABASE_URL ="sqlite+aiosqlite:///:memory:"
    app.db.session.engine = create_async_engine(app.db.session.DATABASE_URL, echo=False, future=True)
    app.db.session.AsyncSessionLocal = sessionmaker(bind=app.db.session.engine, class_=AsyncSession, expire_on_commit=False)

    async with app.db.session.engine.begin() as conn:
        yield await conn.run_sync(Base.metadata.create_all)

    async with app.db.session.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function",)
async def get_db_local_case(init_sqlite_db_local_case):
    async with app.db.session.AsyncSessionLocal() as session:
        yield session
