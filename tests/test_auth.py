import pytest
from httpx import AsyncClient
import json

async def test_create_user(ac: AsyncClient):
    response = await ac.post('/registrate/', json={
            "password": "string",
            "username": "string",
            "mail": "some@gmail.com"
    })
    
    assert response.status_code == 200

async def test_create_user_same_name(ac: AsyncClient):
    response = await ac.post('/registrate/', json={
            "password": "string",
            "username": "string",
            "mail": "another@gmail.com"
    })
    
    assert response.status_code == 400

async def test_create_user_same_email(ac: AsyncClient):
    response = await ac.post('/registrate/', json={
            "password": "string",
            "username": "another",
            "mail": "some@gmail.com"
    })
    
    assert response.status_code == 400

async def test_auth_user_byname(ac: AsyncClient):
    response = await ac.post('/login/', data={
                "username": "string", "password": "string", "grant_type": "password"},
                headers={"content-type": "application/x-www-form-urlencoded"})

    assert response.status_code == 200

refresh_token = ''
access_token = ''

async def test_auth_user_byemail(ac: AsyncClient):
    response = await ac.post('/login/', data={
                "username": "some@gmail.com", "password": "string", "grant_type": "password"},
                headers={"content-type": "application/x-www-form-urlencoded"})
    str = response.text
    data = json.loads(str)
    refresh_token = data["refresh_token"]
    access_token = data["access_token"]
        
    assert response.status_code == 200



async def test_wrong_auth_user_byname(ac: AsyncClient):
    response = await ac.post('/login/', data={
                "username": "notname", "password": "string", "grant_type": "password"},
                headers={"content-type": "application/x-www-form-urlencoded"})

    assert response.status_code == 401

async def test_wrong_auth_user_byemail(ac: AsyncClient):
    response = await ac.post('/login/', data={
                "username": "not@gmail.com", "password": "string", "grant_type": "password"},
                headers={"content-type": "application/x-www-form-urlencoded"})

    assert response.status_code == 401


async def test_refreshtoken(ac: AsyncClient):
    response = await ac.post('/login/refreshtoken')

    assert response.status_code == 200