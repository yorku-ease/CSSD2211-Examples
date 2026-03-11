import pytest
from unittest.mock import MagicMock, patch
import types

@pytest.fixture
def client():
    # Create a fake redis_client module
    fake_redis_module = types.ModuleType("shared.redis_client")
    fake_redis = MagicMock()
    fake_redis_module.r = fake_redis

    # Inject fake module BEFORE importing ratings_service
    with patch.dict("sys.modules", {"shared.redis_client": fake_redis_module}):
        from ratings_service import app

        app.config["TESTING"] = True
        yield app.test_client()

def test_rate_success(client):
    from ratings_service import r  # this is now the fake redis client

    payload = {"username": "alice", "movie_id": "42", "rating": 5}
    response = client.post("/api/rate", json=payload)

    assert response.status_code == 200
    assert response.json == {"status": "ok"}

    r.hset.assert_called_once_with("ratings:alice", "42", 5)

def test_rate_missing_fields(client):
    response = client.post("/api/rate", json={"username": "bob"})
    assert response.status_code == 500

def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"http_requests_total" in response.data