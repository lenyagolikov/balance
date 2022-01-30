import pytest
from fastapi import status
from fastapi.testclient import TestClient

prefix = "users"
trprefix = "transactions"

"""
users_in_db = {1: 100, 2: 200}
"""

data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]

data_transfer = [
    {"from": 1, "to": 2, "amount": 100},
    {"from": 2, "to": 1, "amount": 200},
]


@pytest.mark.parametrize("data", data)
def test_get_transactions_after_deposit(client: TestClient, prepare_db, data: dict):
    resp = client.post(f"/{prefix}/deposit", json=data)
    assert resp.status_code == status.HTTP_201_CREATED

    resp = client.get(f"/{trprefix}/{data['id']}")
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()[0]
    assert body["user_id"] == data["id"]
    assert body["type"] == "deposit"
    assert body["amount"] == data["amount"]


@pytest.mark.parametrize("data", data)
def test_get_transactions_after_withdraw(
    client: TestClient, prepare_db, users_in_db, data: dict
):
    resp = client.post(f"/{prefix}/withdraw", json=data)
    assert resp.status_code == status.HTTP_200_OK

    resp = client.get(f"/{trprefix}/{data['id']}")
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()[0]
    assert body["user_id"] == data["id"]
    assert body["type"] == "withdraw"
    assert body["amount"] == -data["amount"]


@pytest.mark.parametrize("data", data_transfer)
def test_get_transactions_after_transfer(
    client: TestClient, prepare_db, users_in_db, data: dict
):
    resp = client.post(f"/{prefix}/transfer", json=data)
    assert resp.status_code == status.HTTP_200_OK

    resp = client.get(f"/{trprefix}/{data['from']}")
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()[0]
    assert body["user_id"] == data["from"]
    assert body["type"] == "transfer"
    assert body["amount"] == -data["amount"]

    resp = client.get(f"/{trprefix}/{data['to']}")
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()[0]
    assert body["user_id"] == data["to"]
    assert body["type"] == "transfer"
    assert body["amount"] == data["amount"]
