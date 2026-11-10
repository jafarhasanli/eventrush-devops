
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_events(monkeypatch):
    fake_connection = MagicMock()

    fake_connection.execute.return_value.mappings.return_value.all.return_value = [
        {
            "id": 1,
            "title": "Demo Concert",
            "capacity": 100
        }
    ]

    fake_engine = MagicMock()
    fake_engine.connect.return_value.__enter__.return_value = fake_connection

    monkeypatch.setattr(
        "app.main.get_engine",
        lambda: fake_engine
    )

    response = client.get("/events")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Demo Concert",
            "capacity": 100
        }
    ]
