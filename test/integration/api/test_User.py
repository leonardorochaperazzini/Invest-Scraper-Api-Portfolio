import pytest
from fastapi.testclient import TestClient

from app.api import app
from app.model.User import User as UserModelDB
from app.repository.User import User as UserRepository

from app.service.Auth.model.User import User as UserModelService
from app.service.Auth import get_current_active_user

client = TestClient(app)
 
def test_get_current_user():
    user_repository = UserRepository(UserModelDB)
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

    token = response.json()["access_token"]

    response = client.get("/users/me/", headers={"Authorization": f"Bearer {token}"})

    user_repository.delete(user.id)

    assert response.status_code == 200

def test_get_current_disabled_user():
    user_repository = UserRepository(UserModelDB)
    user = user_repository.create({
        "username": "teste",
        "full_name": "teste",
        "email": "teste",
        "hashed_password": "$2a$12$U2KDVI9Z2I89MGMWTE0AguViczK7aAvb1.Q3zRRZ7UQPA8LYdfzcO",
        "disabled": True,
    })

    form_data = {
        "grant_type": "password",
        "username": "teste",
        "password": "teste"
    }

    response = client.post("/auth/token", data=form_data)

    token = response.json()["access_token"]

    response = client.get("/users/me/", headers={"Authorization": f"Bearer {token}"})

    user_repository.delete(user.id)

    assert response.status_code == 400
    assert response.json() == {"detail": "Inactive user"}


async def mock_get_current_active_user():
    return UserModelService(
        username='mock', 
        email="mock@example.com", 
        full_name="mock", 
        disabled=False
    )

@pytest.fixture
def override_dependency():
    # Override da dependência antes dos testes
    app.dependency_overrides[get_current_active_user] = mock_get_current_active_user
    yield
    # Limpar o override após os testes
    app.dependency_overrides = {}

def test_get_current_user_mocked(override_dependency):
    response = client.get("/users/me/")
    assert response.status_code == 200
    assert response.json() == {
        "username": "mock",
        "email": "mock@example.com",
        "full_name": "mock",
        "disabled": False
    }