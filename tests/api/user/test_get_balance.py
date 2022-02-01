import pytest
from fastapi import status
from httpx import AsyncClient

prefix = "users"

data_in_db = {1: 100, 2: 200}

data = [1, 2]
currency_data = [(1, "USD"), (2, "EUR")]


@pytest.mark.parametrize("user_id", data)
async def test_get_user_success(async_client: AsyncClient, db_with_data, user_id: int):
    resp = await async_client.get(f"/{prefix}/{user_id}")
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert data["id"] == user_id
    assert data["balance"] == data_in_db[user_id]


@pytest.mark.parametrize("user_id, currency", currency_data)
async def test_get_user_success_with_currency(
    async_client: AsyncClient, db_with_data, user_id: int, currency: str
):
    resp = await async_client.get(f"/{prefix}/{user_id}?currency={currency}")
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert data["id"] == user_id
    assert data["balance"] < data_in_db[user_id]


@pytest.mark.parametrize("user_id", data)
async def test_get_user_not_found(async_client: AsyncClient, user_id: int):
    resp = await async_client.get(f"/{prefix}/{user_id}")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "user not found"}
