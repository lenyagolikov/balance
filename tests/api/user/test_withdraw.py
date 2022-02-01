import pytest
from fastapi import status
from httpx import AsyncClient

prefix = "users"

data_in_db = {1: 100, 2: 200}

data_withdraw = [
    {"id": 1, "amount": 100},
    {"id": 2, "amount": 200},
]

# данные для теста, когда недостаточно денег
data_withdraw_over = [
    {"id": 1, "amount": 200},
    {"id": 2, "amount": 300},
]


@pytest.mark.parametrize("body", data_withdraw)
async def test_withdraw_success(async_client: AsyncClient, db_with_data, body: dict):
    resp = await async_client.post(f"/{prefix}/withdraw", json=body)
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert data["id"] == body["id"]
    assert data["balance"] == data_in_db[body["id"]] - body["amount"]


@pytest.mark.parametrize("body", data_withdraw)
async def test_withdraw_user_not_found(async_client: AsyncClient, body: dict):
    resp = await async_client.post(f"/{prefix}/withdraw", json=body)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "user not found"}


@pytest.mark.parametrize("body", data_withdraw_over)
async def test_withdraw_not_money(async_client: AsyncClient, db_with_data, body: dict):
    resp = await async_client.post(f"/{prefix}/withdraw", json=body)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "not enough money"}
