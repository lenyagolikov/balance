import pytest
from fastapi import status
from fastapi.testclient import TestClient

prefix = "users"

"""
users_in_db = {1: 100, 2: 200}
"""

data = [1, 2]
currency_data = [(1, "USD"), (2, "EUR")]


@pytest.mark.parametrize("user_id", data)
def test_get_user_success(client: TestClient, prepare_db, users_in_db, user_id: int):
    resp = client.get(f"/{prefix}/{user_id}")
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert data["id"] == user_id
    assert data["balance"] == users_in_db[user_id]


@pytest.mark.parametrize("user_id, currency", currency_data)
def test_get_user_success_with_currency(
    client: TestClient, prepare_db, users_in_db, user_id: int, currency: str
):
    resp = client.get(f"/{prefix}/{user_id}?currency={currency}")
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert data["id"] == user_id
    assert data["balance"] < users_in_db[user_id]


@pytest.mark.parametrize("user_id", data)
def test_get_user_not_found(client: TestClient, prepare_db, user_id: int):
    resp = client.get(f"/{prefix}/{user_id}")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "user not found"}
