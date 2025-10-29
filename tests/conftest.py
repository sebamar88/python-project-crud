import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture(autouse=True)
def bypass_auth(monkeypatch):
    from src.dependencies import auth

    async def fake_get_current_user():
        return {"id": 1, "email": "test@example.com", "role": "admin"}

    app.dependency_overrides[auth.get_current_user] = fake_get_current_user
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)
