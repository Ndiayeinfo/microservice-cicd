# services/gateway/tests/test_gateway.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_gateway_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_gateway_route_forward():
    """Simule un appel proxy vers auth service."""
    response = client.get("/auth/simulated")
    assert response.status_code in [200, 404]
