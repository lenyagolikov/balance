import pytest
from fastapi import status
from httpx import AsyncClient

prefix = "users"
trprefix = "transactions"

data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]

data_transfer = [
    {"from": 1, "to": 2, "amount": 100},
    {"from": 2, "to": 1, "amount": 200},
]

data_limit = [
    ({"id": 1, "amount": 100}, 2),
    ({"id": 1, "amount": 200}, 3),
]


data_limit_offset = [
    ({"id": 1, "amount": 100}, 2, 2),
    ({"id": 1, "amount": 200}, 3, 1),
]


@pytest.mark.parametrize("data", data)
async def test_get_transactions_after_deposit(async_client: AsyncClient, data: dict):
    resp = await async_client.post(f"/{prefix}/deposit", json=data)
    assert resp.status_code == status.HTTP_201_CREATED

    resp = await async_client.get(f"/{trprefix}/{data['id']}")
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()[0]
    assert body["user_id"] == data["id"]
    assert body["type"] == "deposit"
    assert body["amount"] == data["amount"]


@pytest.mark.parametrize("data", data)
async def test_get_transactions_after_withdraw(
    async_client: AsyncClient, db_with_data, data: dict
):
    resp = await async_client.post(f"/{prefix}/withdraw", json=data)
    assert resp.status_code == status.HTTP_200_OK

    resp = await async_client.get(f"/{trprefix}/{data['id']}")
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()[0]
    assert body["user_id"] == data["id"]
    assert body["type"] == "withdraw"
    assert body["amount"] == -data["amount"]


@pytest.mark.parametrize("data", data_transfer)
async def test_get_transactions_after_transfer(
    async_client: AsyncClient, db_with_data, data: dict
):
    resp = await async_client.post(f"/{prefix}/transfer", json=data)
    assert resp.status_code == status.HTTP_200_OK

    resp = await async_client.get(f"/{trprefix}/{data['from']}")
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()[0]
    assert body["user_id"] == data["from"]
    assert body["type"] == "transfer"
    assert body["amount"] == -data["amount"]

    resp = await async_client.get(f"/{trprefix}/{data['to']}")
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()[0]
    assert body["user_id"] == data["to"]
    assert body["type"] == "transfer"
    assert body["amount"] == data["amount"]


@pytest.mark.parametrize("data, limit", data_limit)
async def test_get_transactions_with_limit(
    async_client: AsyncClient, data: dict, limit: int
):
    for _ in range(5):
        await async_client.post(f"/{prefix}/deposit", json=data)

    resp = await async_client.get(f"/{trprefix}/{data['id']}?limit={limit}")
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) == limit


@pytest.mark.parametrize("data, limit, offset", data_limit_offset)
async def test_get_transactions_with_limit_and_offset(
    async_client: AsyncClient, data: dict, limit: int, offset: int
):
    total = 5
    for _ in range(total):
        await async_client.post(f"/{prefix}/deposit", json=data)

    resp = await async_client.get(
        f"/{trprefix}/{data['id']}?limit={limit}&offset={offset}"
    )
    assert resp.status_code == status.HTTP_200_OK

    quantity = total - offset + 1
    quantity = min(quantity, limit)
    assert len(resp.json()) == quantity
