import pytest
from fastapi import status
from fastapi.testclient import TestClient

prefix = "users"

"""
users_in_db = {1: 100, 2: 200}
"""

data_deposit = [
    {"user_id": 1, "value": 100},
    {"user_id": 2, "value": 200},
]

data_first_deposit = [
    {"user_id": 1, "value": 100},
    {"user_id": 2, "value": 200},
]

data_deposit_not_valid = [{"user_id": 1, "value": 0}, {"user_id": 2, "value": -100}]


@pytest.mark.parametrize("body", data_first_deposit)
def test_first_deposit_success(client: TestClient, prepare_db, body: dict):
    resp = client.post(f"/{prefix}/deposit", json=body)
    assert resp.status_code == status.HTTP_201_CREATED

    data = resp.json()
    assert data["user_id"] == body["user_id"]
    assert data["balance"] == body["value"]


@pytest.mark.parametrize("body", data_deposit)
def test_deposit_success(client: TestClient, prepare_db, users_in_db: dict, body: dict):
    resp = client.post(f"/{prefix}/deposit", json=body)
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert data["user_id"] == body["user_id"]
    assert data["balance"] == users_in_db[body["user_id"]] + body["value"]


@pytest.mark.parametrize("body", data_deposit_not_valid)
def test_deposit_not_valid(client: TestClient, body: dict):
    resp = client.post(f"/{prefix}/deposit", json=body)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
