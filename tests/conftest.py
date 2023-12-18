import asyncio
from re import X
from typing import AsyncGenerator

import pytest
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from datetime import timedelta


from app.database.db import get_session
from app.services.jwt import oauth2_scheme, create_access_token
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


oauth2_scheme_override = OAuth2PasswordBearer(tokenUrl="/login/")
app.dependency_overrides[oauth2_scheme] = oauth2_scheme_override
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


@pytest.fixture(scope="session")
async def test_user(ac: AsyncClient):
    response = await ac.post('/registrate/', json={
            "password": "testuser",
            "username": "string",
            "mail": "some@gmail.com"
    })
    
    assert response.status_code == 200

@pytest.fixture(scope="session")
async def token():
    access_token = await create_access_token(
        data={'user_id': 1}, expires_delta=timedelta(minutes=20)
        )
    yield access_token


@pytest.fixture(scope="session")
async def authorized_client(ac: AsyncClient, token):
    ac.headers = {
        **ac.headers,
        "Authorization": f"Bearer {token}"
    }

    return ac