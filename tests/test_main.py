from fastapi.testclient import TestClient
from app.main import app
from app.config import Settings, get_settings

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "app_name" in data
    assert "version" in data
    assert "environment" in data

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_settings():
    settings = get_settings()
    assert isinstance(settings, Settings)
    assert hasattr(settings, "app_name")
    assert hasattr(settings, "version")
    assert hasattr(settings, "debug")
    assert hasattr(settings, "firebase_project_id")
    assert hasattr(settings, "firebase_api_key")
    assert hasattr(settings, "firebase_auth_domain")
    assert hasattr(settings, "firebase_storage_bucket")
    assert hasattr(settings, "allowed_origins") 