from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


def test_register_user_success(client: TestClient):
    mock_user = {"email": "test@example.com", "password": "secure123", "role": "user"}

    with patch(
        "src.router.auth_routes.register_user",
        new=AsyncMock(return_value=mock_user),
    ):
        payload = {"email": "test@example.com", "password": "secure123", "role": "user"}
        response = client.post("/auth/register", json=payload)

    assert response.status_code == 200
    assert response.json() == {"user": mock_user}


def test_login_success(client: TestClient):
    mock_token = {"access_token": "fake.jwt.token", "token_type": "bearer"}

    with patch(
        "src.router.auth_routes.login_user",
        new=AsyncMock(return_value=mock_token),
    ):
        payload = {"email": "user@example.com", "password": "1234"}
        response = client.post("/auth/login", json=payload)

    assert response.status_code == 200
    assert response.json() == mock_token


def test_login_invalid_credentials(client: TestClient):
    with patch(
        "src.router.auth_routes.login_user",
        new=AsyncMock(return_value=None),
    ):
        payload = {"email": "wrong@example.com", "password": "bad"}
        response = client.post("/auth/login", json=payload)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
