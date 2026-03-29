from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_sheep():
    response = client.get("/sheep/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1, "name": "Spice", "breed": "Gotland", "sex": "ewe"
    }


def test_read_all_sheep():
    response = client.get("/sheep")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6
    assert data[0]["name"] == "Spice"


def test_update_sheep():
    updated_sheep = {
        "id": 1, "name": "SpiceUpdated", "breed": "Gotland", "sex": "ewe"
    }
    response = client.put("/sheep/1", json=updated_sheep)
    assert response.status_code == 200
    assert response.json()["name"] == "SpiceUpdated"

    get_response = client.get("/sheep/1")
    assert get_response.json()["name"] == "SpiceUpdated"


def test_delete_sheep():
    response = client.delete("/sheep/1")
    assert response.status_code == 204

    get_response = client.get("/sheep/1")
    assert get_response.status_code == 404