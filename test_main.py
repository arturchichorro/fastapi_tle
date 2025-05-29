import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

valid_line1 = "1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927"
valid_line2 = "2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"
invalid_line1 = "1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0   2927"

def test_empty_request_body():
    response = client.post("/position", json={})
    assert response.status_code == 422
    assert "line1" in response.text and "line2" in response.text


def test_valid_tle_with_timestamp():
    response = client.post("/position", json={
        "line1": valid_line1,
        "line2": valid_line2,
        "timestamp": "2024-01-01T12:00:00"
    })
    assert response.status_code == 200
    data = response.json()
    assert all(key in data for key in ["x", "y", "z"])
    assert isinstance(data["x"], float)

def test_valid_tle_without_timestamp():
    response = client.post("/position", json={
        "line1": valid_line1,
        "line2": valid_line2
    })
    assert response.status_code == 200
    data = response.json()
    assert all(key in data for key in ["x", "y", "z"])

def test_invalid_tle_format():
    response = client.post("/position", json={
        "line1": "invalid",
        "line2": "also invalid"
    })
    assert response.status_code == 400
    assert "TLE" in response.json()["detail"]

def test_tle_line_too_long():
    invalid_line1 = "1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0   2927"
    response = client.post("/position", json={
        "line1": invalid_line1,
        "line2": valid_line2
    })
    assert response.status_code == 400
    assert "69 characters" in response.json()["detail"]


def test_invalid_tle_checksum():
    bad_checksum_line1 = valid_line1[:-1] + "1"
    response = client.post("/position", json={
        "line1": bad_checksum_line1,
        "line2": valid_line2
    })
    assert response.status_code == 400
    assert "checksum" in response.json()["detail"]

def test_invalid_timestamp_format():
    response = client.post("/position", json={
        "line1": valid_line1,
        "line2": valid_line2,
        "timestamp": "not-a-date"
    })
    assert response.status_code == 422
