import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.schemas import User

prefix = "users"

data_withdraw = [
    {"user_id": 1, "value": 100},
    {"user_id": 2, "value": 200},
]

# данные для теста, когда недостаточно денег
data_withdraw_over = [
    {"user_id": 1, "value": 200},
    {"user_id": 2, "value": 300},
]


@pytest.mark.parametrize("body", data_withdraw)
def test_withdraw_success(client: TestClient, add_data_to_db, body: dict):
    resp = client.post(f"/{prefix}/withdraw", json=body)
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert data == User(**data)


@pytest.mark.parametrize("body", data_withdraw)
def test_withdraw_user_not_found(client: TestClient, body: dict):
    resp = client.post(f"/{prefix}/withdraw", json=body)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "user not found"}


@pytest.mark.parametrize("body", data_withdraw_over)
def test_withdraw_not_money(client: TestClient, add_data_to_db, body: dict):
    resp = client.post(f"/{prefix}/withdraw", json=body)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "not enough money"}
