from fastapi.testclient import TestClient
from unittest.mock import patch
import pytest
import uuid
from app.routers.users import users_db
from app.routers.posts import posts_db
from .main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    users_db.clear()
    posts_db.clear()
    yield


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API"}


@pytest.fixture(autouse=True)
def mock_uuid():
    with patch('uuid.uuid4') as mock_uuid:
        mock_uuid.return_value = uuid.UUID('12345678-1234-5678-1234-567812345678')
        yield


def test_create_user():
    response = client.post("/users/", json={"name": "test", "email": "test@email.address"})

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == "test"


def test_get_user():
    response = client.post("/users/", json={"name": "test", "email": "test@email.address"})
    user_id = response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"id": user_id, "name": "test", "email": "test@email.address"}


def test_get_users():
    response = client.post("/users/", json={"name": "test", "email": "test@email.address"})
    user_id = response.json()["id"]

    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [{"id": user_id, "name": "test", "email": "test@email.address"}]


def test_update_user():
    response = client.post("/users/", json={"name": "test", "email": "test@email.address"})
    user_id = response.json()["id"]

    response = client.put(f"/users/{user_id}", json={"name": "updated", "email": "test@email.address"})
    assert response.status_code == 200
    assert response.json() == {"id": user_id, "name": "updated", "email": "test@email.address"}


def test_delete_user():
    response = client.post("/users/", json={"name": "test", "email": "test@email.address"})
    user_id = response.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_create_post():
    response = client.post("/users/", json={"name": "test", "email": "a@a.a"})
    user_id = response.json()["id"]

    response = client.post("/posts/", json={"title": "test", "content": "test content", "user_id": user_id})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["title"] == "test"


def test_get_posts():
    response = client.post("/users/", json={"name": "test", "email": "test@email.address"})
    user_id = response.json()["id"]
    response = client.post("/posts/", json={"title": "test", "content": "test content", "user_id": user_id})
    post_id = response.json()["id"]

    response = client.get("/posts/")
    assert response.status_code == 200
    assert response.json() == [{"id": post_id, "title": "test", "content": "test content", "user_id": user_id}]


def test_get_post():
    response = client.post("/users/", json={"name": "test", "email": "test@email.address"})
    user_id = response.json()["id"]
    response = client.post("/posts/", json={"title": "test", "content": "test content", "user_id": user_id})
    post_id = response.json()["id"]

    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json() == {"id": post_id, "title": "test", "content": "test content", "user_id": user_id}


def test_update_post():
    response = client.post("/users/", json={"name": "test", "email": "test@email.address"})
    user_id = response.json()["id"]
    response = client.post("/posts/", json={"title": "test", "content": "test content", "user_id": user_id})
    post_id = response.json()["id"]

    response = client.put(f"/posts/{post_id}", json={"title": "updated", "content": "updated content", "user_id": user_id})
    assert response.status_code == 200
    assert response.json() == {"id": post_id, "title": "updated", "content": "updated content", "user_id": user_id}


def test_delete_post():
    response = client.post("/users/", json={"name": "test", "email": "test@email.address"})
    user_id = response.json()["id"]
    response = client.post("/posts/", json={"title": "test", "content": "test content", "user_id": user_id})
    post_id = response.json()["id"]

    print(response.json())
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 204
    print("going")
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 404


def test_missing_user():
    # use mock uuid
    uuid = "12345678-1234-5678-1234-567812345678"
    response = client.post("/posts/", json={"title": "test", "content": "test content", "user_id": uuid})
    assert response.status_code == 404

