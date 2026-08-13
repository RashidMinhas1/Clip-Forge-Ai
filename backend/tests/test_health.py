import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "version" in data
    assert "timestamp" in data

def test_readiness_check():
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "dependencies" in data
    assert data["dependencies"]["redis"] == "simulated_connected"
    assert data["dependencies"]["postgres"] == "simulated_connected"
