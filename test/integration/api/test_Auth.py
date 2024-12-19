import pytest
from fastapi.testclient import TestClient

from app.api import app
from app.model.User import User as UserModel
from app.repository.User import User as UserRepository
client = TestClient(app)

def test_auth_invalid_password():
    form_data = {
        "grant_type": "password",
        "username": "lperazzini",
        "password": "secret"
    }
    
    response = client.post("/auth/token", data=form_data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_auth_invalid_username():
    form_data = {
        "grant_type": "password",
        "username": "teste",
        "password": "secret"
    }
    
    response = client.post("/auth/token", data=form_data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_auth_request_missing_parameters():
    response = client.post("/auth/token", data={})

    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {'type': 'missing', 'loc': ['body', 'username'], 'msg': 'Field required', 'input': None}, 
            {'type': 'missing', 'loc': ['body', 'password'], 'msg': 'Field required', 'input': None}
        ]
    }

def test_auth_is_valid():
    user_repository = UserRepository(UserModel)
    user = user_repository.create({
        "username": "teste",
        "full_name": "teste",
        "email": "teste",
        "hashed_password": "$2a$12$U2KDVI9Z2I89MGMWTE0AguViczK7aAvb1.Q3zRRZ7UQPA8LYdfzcO",
        "disabled": False,
    })

    form_data = {
        "grant_type": "password",
        "username": "teste",
        "password": "teste"
    }

    response = client.post("/auth/token", data=form_data)

    user_repository.delete(user.id)

    assert response.status_code == 200