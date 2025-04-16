from unittest.mock import patch

import pytest
from app.config import Settings, get_settings
from app.main import app
from app.models.user import UserCreate, UserResponse
from app.services.firebase_service import FirebaseService
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture
def mock_firebase_service():
    with patch("app.services.firebase_service.FirebaseService") as mock:
        yield mock


def test_register_user_success(mock_firebase_service):
    # Mock successful user creation
    mock_firebase_service.return_value.create_user.return_value = {
        "uid": "test123",
        "email": "test@example.com",
        "display_name": "Test User",
    }

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPass123!",
            "display_name": "Test User",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert "uid" in response.json()


def test_register_user_invalid_email(mock_firebase_service):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "invalid-email",
            "password": "TestPass123!",
            "display_name": "Test User",
        },
    )

    assert response.status_code == 422
    assert "email" in response.json()["detail"][0]["loc"]


def test_register_user_weak_password(mock_firebase_service):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "weak",
            "display_name": "Test User",
        },
    )

    assert response.status_code == 422
    assert "password" in response.json()["detail"][0]["loc"]


def test_login_success(mock_firebase_service):
    # Mock successful login
    mock_firebase_service.return_value.verify_id_token.return_value = {
        "uid": "test123",
        "email": "test@example.com",
    }

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "TestPass123!"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_invalid_credentials(mock_firebase_service):
    # Mock failed login
    mock_firebase_service.return_value.verify_id_token.side_effect = Exception(
        "Invalid credentials"
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "WrongPass123!"},
    )

    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


def test_refresh_token_success(mock_firebase_service):
    # Mock successful token refresh
    mock_firebase_service.return_value.verify_id_token.return_value = {
        "uid": "test123",
        "email": "test@example.com",
    }

    response = client.post(
        "/api/v1/auth/refresh", json={"refresh_token": "valid-refresh-token"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_current_user_success(mock_firebase_service):
    # Mock successful user retrieval
    mock_firebase_service.return_value.get_user.return_value = {
        "uid": "test123",
        "email": "test@example.com",
        "display_name": "Test User",
        "email_verified": True,
        "disabled": False,
    }

    # First get a valid token
    mock_firebase_service.return_value.verify_id_token.return_value = {
        "uid": "test123",
        "email": "test@example.com",
    }

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "TestPass123!"},
    )

    token = login_response.json()["access_token"]

    # Then use the token to get user info
    response = client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["uid"] == "test123"


def test_protected_route_access(mock_firebase_service):
    # Mock successful token verification
    mock_firebase_service.return_value.verify_id_token.return_value = {
        "uid": "test123",
        "email": "test@example.com",
    }

    # First get a valid token
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "TestPass123!"},
    )

    token = login_response.json()["access_token"]

    # Try to access a protected route
    response = client.get(
        "/api/v1/protected-route", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_protected_route_no_token(mock_firebase_service):
    response = client.get("/api/v1/protected-route")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_protected_route_invalid_token(mock_firebase_service):
    # Mock failed token verification
    mock_firebase_service.return_value.verify_id_token.side_effect = Exception(
        "Invalid token"
    )

    response = client.get(
        "/api/v1/protected-route", headers={"Authorization": "Bearer invalid-token"}
    )

    assert response.status_code == 401
    assert "Invalid token" in response.json()["detail"]


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "display_name": "Test User",
            "photo_url": "https://example.com/photo.jpg",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "uid" in data
    assert data["email"] == "test@example.com"
    assert data["display_name"] == "Test User"


def test_login():
    response = client.post(
        "/auth/token", data={"username": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
