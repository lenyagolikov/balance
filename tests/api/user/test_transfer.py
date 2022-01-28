import pytest
from fastapi import status
from fastapi.testclient import TestClient

"""
`add_data_to_db` вносит в БД:
id: 1, balance: 100
id: 2, balance: 200
"""

prefix = "users"

data_transfer = [
    {"from": 1, "to": 2, "value": 100},
    {"from": 2, "to": 1, "value": 200},
]

data_transfer_not_money = [
    {"from": 1, "to": 2, "value": 200},
    {"from": 2, "to": 1, "value": 300},
]

data_transfer_sender_not_found = [
    {"from": 3, "to": 1, "value": 100}
]

data_transfer_receiver_not_found = [
    {"from": 1, "to": 3, "value": 100}
]


@pytest.mark.parametrize("body", data_transfer)
def test_transfer_success(client: TestClient, add_data_to_db, body: dict):
    resp = client.post(f"/{prefix}/transfer", json=body)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"detail": "Success"}


@pytest.mark.parametrize("body", data_transfer_sender_not_found)
def test_transfer_sender_not_found(client: TestClient, add_data_to_db, body: dict):
    resp = client.post(f"/{prefix}/transfer", json=body)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "sender not found"}


@pytest.mark.parametrize("body", data_transfer_receiver_not_found)
def test_transfer_receiver_not_found(client: TestClient, add_data_to_db, body: dict):
    resp = client.post(f"/{prefix}/transfer", json=body)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "receiver not found"}


@pytest.mark.parametrize("body", data_transfer_not_money)
def test_transfer_not_money(client: TestClient, add_data_to_db, body: dict):
    resp = client.post(f"/{prefix}/transfer", json=body)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "not enough money"}
