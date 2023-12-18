from re import A
from urllib import response
import pytest
from httpx import AsyncClient

async def test_create_track(authorized_client):
    response = await authorized_client.post('/track/', json={
  "name": "string",
  "description": "string"
})
    
    assert response.status_code == 200

async def test_create_same_track(authorized_client):
    response = await authorized_client.post('/track/', json={
  "name": "string",
  "description": "string"
})
    
    assert response.status_code == 400

async def test_get_user_tracks(authorized_client):
    response = await authorized_client.get('/track/get_user_tracks')

    assert response.status_code == 200

async def test_get_user_track(authorized_client):
    response = await authorized_client.get('/track/get_user_track', params={
        'track_id': 1
    })
    
    assert response.status_code == 200

async def test_get_user_track_not_exist(authorized_client):
    response = await authorized_client.get('/track/get_user_track', params={
        'track_id': 5
    })

    assert response.status_code == 200
    assert response.text == "null"

async def test_add_time_to_track(authorized_client):
    response = await authorized_client.put('/track/add_time', params={
        'track_id': 1,
        'time': 100
    })

    assert response.status_code == 200

async def test_add_time_to_not_exist_track(authorized_client):
    response = await authorized_client.put('/track/add_time', params={
        'track_id': 3,
        'time': 100
    })

    assert response.status_code == 400

async def test_disable_track(authorized_client):
    response = await authorized_client.put('/track/disable_track', params={
        'track_id': 1
    })

    assert response.status_code == 200

async def test_disable_track_not_exist(authorized_client):
    response = await authorized_client.put('/track/disable_track', params={
        'track_id': 4
    })

    assert response.status_code == 400