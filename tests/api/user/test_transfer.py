import pytest
from fastapi import status
from httpx import AsyncClient

prefix = "users"

data_in_db = {1: 100, 2: 200}

data_transfer = [
    {"from": 1, "to": 2, "amount": 100},
    {"from": 2, "to": 1, "amount": 200},
]

data_transfer_not_money = [
    {"from": 1, "to": 2, "amount": 200},
    {"from": 2, "to": 1, "amount": 300},
]

data_transfer_sender_not_found = [{"from": 3, "to": 1, "amount": 100}]

data_transfer_receiver_not_found = [{"from": 1, "to": 3, "amount": 100}]


@pytest.mark.parametrize("body", data_transfer)
async def test_transfer_success(async_client: AsyncClient, db_with_data, body: dict):
    resp = await async_client.post(f"/{prefix}/transfer", json=body)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"detail": "Success"}


@pytest.mark.parametrize("body", data_transfer_sender_not_found)
async def test_transfer_sender_not_found(
    async_client: AsyncClient, db_with_data, body: dict
):
    resp = await async_client.post(f"/{prefix}/transfer", json=body)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "sender not found"}


@pytest.mark.parametrize("body", data_transfer_receiver_not_found)
async def test_transfer_receiver_not_found(
    async_client: AsyncClient, db_with_data, body: dict
):
    resp = await async_client.post(f"/{prefix}/transfer", json=body)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "receiver not found"}


@pytest.mark.parametrize("body", data_transfer_not_money)
async def test_transfer_not_money(async_client: AsyncClient, db_with_data, body: dict):
    resp = await async_client.post(f"/{prefix}/transfer", json=body)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "not enough money"}
