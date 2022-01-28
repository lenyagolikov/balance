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


@pytest.mark.parametrize("user_id", [1, 2])
def test_get_user_success(client: TestClient, add_data_to_db, user_id: int):
    resp = client.get(f"/{prefix}/{user_id}")
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert data == User(**data)


@pytest.mark.parametrize("user_id", [1, 2])
def test_get_user_not_found(client: TestClient, user_id: int):
    resp = client.get(f"/{prefix}/{user_id}")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "user not found"}
