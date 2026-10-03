from fastapi.testclient import TestClient

from app import app, monitor

client = TestClient(app, raise_server_exceptions=False)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "API Performance Monitor is running"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_metrics_include_recorded_requests():
    client.get("/health")
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data
    assert "average_response_time_ms" in data
    assert "endpoints" in data
    assert any(item["endpoint"] == "GET /health" for item in data["endpoints"])


def test_error_endpoint_is_counted():
    client.get("/error")
    data = client.get("/metrics").json()
    assert data["error_count"] >= 1


def test_dashboard_loads():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "API Performance Monitor" in response.text
