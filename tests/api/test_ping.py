from fastapi import status
from fastapi.testclient import TestClient

prefix = "ping"


def test_ping_app_up(client: TestClient):
    resp = client.get(f"/{prefix}/app")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"detail": "app is up"}


def test_ping_db_up(client: TestClient):
    resp = client.get(f"/{prefix}/db")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"detail": "db is up"}


def test_ping_db_down(client_with_db_down: TestClient):
    resp = client_with_db_down.get(f"/{prefix}/db")
    assert resp.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert resp.json() == {"detail": "db is down"}
