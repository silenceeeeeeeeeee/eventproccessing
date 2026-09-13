import json
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

with open("events.json", "r", encoding="utf-8") as file:
    events = json.load(file)


def test_valid_event():
    response = client.post("/events", json=events[0])

    assert response.status_code == 200
    assert response.json()["accepted"] is True
    assert response.json()["occupancy_category"] == "MEDIUM"


def test_stopped_event_with_nonzero_speed():
    event = events[0].copy()
    event["status"] = "STOPPED" 
    event["speed_kmh"] = 30

    response = client.post("/events", json=event)

    assert response.status_code == 200
    assert response.json()["accepted"] is False


def test_negative_passengers():
    event = events[0].copy()
    event["passengers"] = -5

    response = client.post("/events", json=event)

    assert response.status_code == 200
    assert response.json()["accepted"] is False