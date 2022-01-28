import pytest
from fastapi import status
from fastapi.testclient import TestClient

prefix = "users"

"""
users_in_db = {1: 100, 2: 200}
"""


@pytest.mark.parametrize("user_id", [1, 2])
def test_get_user_success(client: TestClient, users_in_db, user_id: int):
    resp = client.get(f"/{prefix}/{user_id}")
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    assert data["user_id"] == user_id
    assert data["balance"] == users_in_db[user_id]


@pytest.mark.parametrize("user_id", [1, 2])
def test_get_user_not_found(client: TestClient, user_id: int):
    resp = client.get(f"/{prefix}/{user_id}")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == {"detail": "user not found"}
