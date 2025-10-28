from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_get_customers_success(client: TestClient) -> None:
    customers_data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ]

    with patch(
        "src.router.customer_routes.fetch_customers",
        new=AsyncMock(return_value=customers_data),
    ):
        response = client.get("/customers/")

    assert response.status_code == 200
    assert response.json() == {"customers": customers_data}


def test_get_customer_found(client: TestClient) -> None:
    customer = {"id": 1, "name": "Alice", "email": "alice@example.com"}

    with patch(
        "src.router.customer_routes.fetch_customer_by_id",
        new=AsyncMock(return_value=customer),
    ):
        response = client.get("/customers/1")

    assert response.status_code == 200
    assert response.json() == {"customer": customer}


def test_get_customer_not_found(client: TestClient) -> None:
    with patch(
        "src.router.customer_routes.fetch_customer_by_id",
        new=AsyncMock(return_value=None),
    ):
        response = client.get("/customers/999")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data == [{"error": "Customer not found"}, 404]


def test_create_customer_success(client: TestClient) -> None:
    new_customer = {
        "id": 3,
        "name": "Charlie",
        "email": "charlie@example.com",
        "phone": None,
        "address": None,
        "nickname": None,
    }
    payload = {
        "name": "Charlie",
        "email": "charlie@example.com",
        "phone": None,
        "address": None,
        "nickname": None,
    }

    with patch(
        "src.router.customer_routes.register_new_customer",
        new=AsyncMock(return_value=new_customer),
    ):
        response = client.post("/customers/", json=payload)

    assert response.status_code == 200
    assert response.json() == {"customer": new_customer}


def test_update_customer_success(client: TestClient) -> None:
    updated_customer = {
        "id": 1,
        "name": "Alice Updated",
        "email": "alice@example.com",
        "phone": "123456789",
        "address": "123 Street",
        "nickname": "Al",
    }
    payload = {
        "name": "Alice Updated",
        "email": "alice@example.com",
        "phone": "123456789",
        "address": "123 Street",
        "nickname": "Al",
    }

    with patch(
        "src.router.customer_routes.update_customer_repo",
        new=AsyncMock(return_value=updated_customer),
    ):
        response = client.put("/customers/1", json=payload)

    assert response.status_code == 200
    assert response.json() == {"customer": updated_customer}


def test_update_customer_not_found(client: TestClient) -> None:
    payload = {"name": "Missing"}

    with patch(
        "src.router.customer_routes.update_customer_repo",
        new=AsyncMock(return_value=None),
    ):
        response = client.put("/customers/999", json=payload)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data == [{"error": "Customer not found"}, 404]


def test_delete_customer_success(client: TestClient) -> None:
    with patch(
        "src.router.customer_routes.delete_customer_repo",
        new=AsyncMock(return_value=True),
    ):
        response = client.delete("/customers/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Customer deleted successfully"}


def test_delete_customer_not_found(client: TestClient) -> None:
    with patch(
        "src.router.customer_routes.delete_customer_repo",
        new=AsyncMock(return_value=False),
    ):
        response = client.delete("/customers/999")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data == [{"error": "Customer not found"}, 404]
