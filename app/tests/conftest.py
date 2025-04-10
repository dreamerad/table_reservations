import os
import pytest
import asyncio
from sqlalchemy import text

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app
from app.api.deps import get_db
from fastapi.testclient import TestClient

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


def setup_test_db():
    if os.path.exists("./test.db"):
        os.remove("./test.db")

    engine = create_async_engine(TEST_DATABASE_URL)

    async def _create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_create_tables())

    return engine


# Инициализируем БД перед запуском тестов
test_engine = setup_test_db()
TestingSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def clean_db():

    async def _clean_tables():
        async with TestingSessionLocal() as session:
            await session.execute(text("DELETE FROM reservations"))
            await session.execute(text("DELETE FROM tables"))
            await session.commit()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_clean_tables())


@pytest.fixture
def async_db_session():

    async def _get_session():
        async with TestingSessionLocal() as session:

            await session.execute(text("DELETE FROM reservations"))
            await session.execute(text("DELETE FROM tables"))
            await session.commit()
            return session

    loop = asyncio.get_event_loop()
    session = loop.run_until_complete(_get_session())

    yield session

    loop.run_until_complete(session.close())