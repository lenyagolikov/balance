import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.schemas import User

"""
`add_data_to_db` вносит в БД:
id: 1, balance: 100
id: 2, balance: 200
"""

prefix = "users"

data_deposit = [
    {"user_id": 1, "value": 100},
    {"user_id": 2, "value": 200},
]

data_first_deposit = [
    {"user_id": 1, "value": 100},
    {"user_id": 2, "value": 200},
]

data_deposit_not_valid = [
    {"user_id": 1, "value": 0},
    {"user_id": 2, "value": -100}
]


def deposit(client: TestClient, body: dict, status: status):
    resp = client.post(f"/{prefix}/deposit", json=body)
    assert resp.status_code == status

    data = resp.json()
    assert data == User(**data)


@pytest.mark.parametrize("body", data_first_deposit)
def test_first_deposit_success(client: TestClient, body: dict):
    deposit(client, body, status.HTTP_201_CREATED)


@pytest.mark.parametrize("body", data_deposit)
def test_deposit_success(client: TestClient, add_data_to_db, body: dict):
    deposit(client, body, status.HTTP_200_OK)


@pytest.mark.parametrize("body", data_deposit_not_valid)
def test_deposit_not_valid(client: TestClient, body: dict):
    resp = client.post(f"/{prefix}/deposit", json=body)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
