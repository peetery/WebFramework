import pytest
import requests
import threading
from app import app, db

BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture(scope="module", autouse=True)
def setup_server():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()

    server = threading.Thread(target=app.run, kwargs={"port": 5000, "use_reloader": False}, daemon=True)
    server.start()

    yield

    with app.app_context():
        db.drop_all()


def test_api_get_data():
    response = requests.get(f"{BASE_URL}/api/data")
    assert response.status_code == 200
    assert response.json() == []

    for i in range(3):
        payload = {
            "feature1": 1.0 + i,
            "feature2": 2.0 + i,
            "category": i + 1
        }
        response = requests.post(f"{BASE_URL}/api/data", json=payload)
        assert response.status_code == 201

    response = requests.get(f"{BASE_URL}/api/data")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_api_post_data():
    payload = {"feature1": 1.23, "feature2": 4.56, "category": 2}
    response = requests.post(f"{BASE_URL}/api/data", json=payload)
    assert response.status_code == 201
    record_id = response.json().get("id")
    assert record_id is not None

    response = requests.get(f"{BASE_URL}/api/data")
    assert response.status_code == 200
    data = response.json()
    record = next((item for item in data if item["id"] == record_id), None)
    assert record is not None
    assert record["feature1"] == 1.23
    assert record["feature2"] == 4.56
    assert record["category"] == 2

    invalid_payload = {"feature1": 1.23, "feature2": 4.56}
    response = requests.post(f"{BASE_URL}/api/data", json=invalid_payload)
    assert response.status_code == 400
    assert "error" in response.json()


def test_api_delete_data():
    payload = {"feature1": 1.23, "feature2": 4.56, "category": 2}
    response = requests.post(f"{BASE_URL}/api/data", json=payload)
    assert response.status_code == 201
    record_id = response.json().get("id")

    response = requests.delete(f"{BASE_URL}/api/data/{record_id}")
    assert response.status_code == 200
    assert response.json().get("id") == record_id

    response = requests.get(f"{BASE_URL}/api/data")
    data = response.json()
    assert all(record["id"] != record_id for record in data)

    response = requests.delete(f"{BASE_URL}/api/data/9999")
    assert response.status_code == 404
    assert "error" in response.json()