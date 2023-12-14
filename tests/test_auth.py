import pytest
import time
from httpx import AsyncClient

async def test_create_user(ac: AsyncClient):
    response = await ac.post('/registrate/', json={
            "password": "string",
            "username": "string",
            "mail": "some@gmail.com"
    })
    
    assert response.status_code == 200

