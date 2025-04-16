import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import Settings, get_settings

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def settings():
    return get_settings() 