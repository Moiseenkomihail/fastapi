import asyncio
from email.mime import base
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.database.db import get_session
from app.database.DBmodel import Base
from app.main import app


DB_HOST_T='127.0.0.1'
DB_PORT_T='5432'
DB_NAME_T='test'
DB_PASS_T='postgres'
DB_USER_T='postgres'

TEST_DB_URL = f"postgresql+asyncpg://{DB_USER_T}:{DB_PASS_T}@{DB_HOST_T}:{DB_PORT_T}/{DB_NAME_T}"


engine_test = create_async_engine(
            url=TEST_DB_URL,
            poolclass=NullPool,
)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

metadata = Base.metadata

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_session] = override_get_async_session

@pytest.fixture(autouse=True, scope='session')  
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)

# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

client = TestClient(app)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

