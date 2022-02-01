import pytest
from fastapi import status
from httpx import AsyncClient

prefix = "users"

data_in_db = {1: 100, 2: 200}

data_deposit = [
    {"id": 1, "amount": 100},
    {"id": 2, "amount": 200},
]

data_first_deposit = [
    {"id": 1, "amount": 100},
    {"id": 2, "amount": 200},
]

data_deposit_not_valid = [{"id": 1, "amount": 0}, {"id": 2, "amount": -100}]


@pytest.mark.parametrize("body", data_first_deposit)
async def test_first_deposit_success(async_client: AsyncClient, body: dict):
    resp = await async_client.post(f"/{prefix}/deposit", json=body)
    assert resp.status_code == status.HTTP_201_CREATED

    data = resp.json()
    assert data["id"] == body["id"]
    assert data["balance"] == body["amount"]


@pytest.mark.parametrize("body", data_deposit)
async def test_deposit_success(async_client: AsyncClient, db_with_data, body: dict):
    resp = await async_client.post(f"/{prefix}/deposit", json=body)
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert data["id"] == body["id"]
    assert data["balance"] == data_in_db[body["id"]] + body["amount"]


@pytest.mark.parametrize("body", data_deposit_not_valid)
async def test_deposit_not_valid(async_client: AsyncClient, body: dict):
    resp = await async_client.post(f"/{prefix}/deposit", json=body)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
