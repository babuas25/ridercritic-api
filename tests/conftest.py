import pytest
from functions.app.config import Settings, get_settings
from functions.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def settings():
    return get_settings()
