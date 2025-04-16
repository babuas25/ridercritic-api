from app.config import Settings, get_settings
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_current_user():
    # First, get a token
    login_response = client.post(
        "/auth/token", data={"username": "test@example.com", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]

    # Then use the token to get user info
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert "uid" in data
    assert data["email"] == "test@example.com"


def test_update_current_user():
    # First, get a token
    login_response = client.post(
        "/auth/token", data={"username": "test@example.com", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]

    # Then use the token to update user info
    response = client.put(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "display_name": "Updated Name",
            "photo_url": "https://example.com/new-photo.jpg",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["display_name"] == "Updated Name"
    assert data["photo_url"] == "https://example.com/new-photo.jpg"
