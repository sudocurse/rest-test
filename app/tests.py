from fastapi import FastAPI
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API"}

def test_create_user():
    response = client.post(
        "/users/",
        json={"id": 1, "name": "test", "email": "test@email.address"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "test", "email": "test@email.address"}

def test_get_users():
    # create
    response = client.post(
        "/users/",
        json={"id": 1, "name": "test", "email": "test@email.address"}
    )
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "test", "email": "test@email.address"}]

def test_update_user():
    # create
    response = client.post(
        "/users/",
        json={"id": 1, "name": "test", "email": "test@email.address"}
    )
    # update
    response = client.put(
        "/users/1",
        json={"id": 1, "name": "updated", "email": "test@email.address"}
    )
    assert response.json() == {"id": 1, "name": "updated", "email": "test@email.address"}

def test_delete_user():
    email = "test@email.address"
    # create
    response = client.post(
        "/users/",
        json={"id": 1, "name": "test", "email": email}
    )
    # delete
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
