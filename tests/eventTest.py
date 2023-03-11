import pytest
import json
from app.services.event import EventService


@pytest.fixture
def client():
    app = create_app("test")
    with app.test_client() as client:
        yield client


def test_get_active_events(client):
    response = client.get("/api/events/active")
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("address" in item for item in data)
    assert all("price" in item for item in data)
    assert all("description" in item for item in data)
    assert all("start_date" in item for item in data)
    assert all("end_date" in item for item in data)
    assert all("target_amount" in item for item in data)


def test_get_active_events_with_limit(client):
    response = client.get("/api/events/active?limit=2")
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert isinstance(data, list)
    assert len(data) == 2
    assert all("address" in item for item in data)
    assert all("price" in item for item in data)
    assert all("description" in item for item in data)
    assert all("start_date" in item for item in data)
    assert all("end_date" in item for item in data)
    assert all("target_amount" in item for item in data)


def test_get_event_by_id(client):
    event_service = EventService()
    event = event_service.create_event(
        "123 Main Street",
        100000,
        "Newly renovated single-family home",
        "2023-01-01",
        "2024-01-01",
        200000,
    )
    response = client.get(f"/api/events/{event.id}")
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert isinstance(data, dict)
    assert data["address"] == "123 Main Street"
    assert data["price"] == 100000
    assert data["description"] == "Newly renovated single-family home"
    assert data["start_date"] == "2023-01-01"
    assert data["end_date"] == "2024-01-01"
    assert data["target_amount"] == 200000
