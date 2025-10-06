from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Health API service is running"


def test_health_endpoint_status():
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    expected_keys = {"status", "cpu_percent", "memory_percent", "disk_percent", "timestamp"}
    assert set(data.keys()) == expected_keys, f"Unexpected keys: {data.keys()}"

    # Verify thresholds give a valid status
    assert data["status"] in ["healthy", "unhealthy"]
    assert 0 <= data["cpu_percent"] <= 100, f"Invalid CPU %: {data['cpu_percent']}"
    assert 0 <= data["memory_percent"] <= 100, f"Invalid Memory %: {data['memory_percent']}"
    assert 0 <= data["disk_percent"] <= 100, f"Invalid Disk %: {data['disk_percent']}"


def test_metrics_endpoint_structure():
    response = client.get("/metrics")
    assert response.status_code == 200

    data = response.json()
    assert "cpu" in data
    assert "memory" in data
    assert "disk" in data

    # Validate CPU structure
    cpu = data["cpu"]
    assert all(key in cpu for key in ["percent", "cores", "load_avg", "load_avg_percent"])

    # Validate memory structure
    memory = data["memory"]
    assert all(key in memory for key in ["total", "available", "percent"])

    # Validate disk structure
    disk = data["disk"]
    assert all(key in disk for key in ["total", "used", "free", "percent"])
