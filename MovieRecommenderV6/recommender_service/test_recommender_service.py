import types

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    # Create a fake redis_client module
    fake_redis_module = types.ModuleType("shared.redis_client")
    fake_redis = MagicMock()
    fake_redis_module.r = fake_redis

    # Fake recommender module (to avoid importing scikit-learn)
    fake_recommender_module = types.ModuleType("recommender")
    def fake_recommend(username, ratings_dict, top_n=5):
        if username == "unknown":
            return None
        return pd.Series({"movieA": 4.5, "movieB": 3.2})

    fake_recommender_module.recommend = MagicMock(side_effect=fake_recommend)

    # Inject fake modules BEFORE importing ratings_service
    with patch.dict("sys.modules", {
        "shared.redis_client": fake_redis_module,
        "recommender": fake_recommender_module
    }):
        from recommender_service import app

        app.config["TESTING"] = True
        yield app.test_client()

def test_recommend_success(client):
    from recommender_service import r

    # Fake Redis data
    r.keys.return_value = ["ratings:alice", "ratings:bob"]
    r.hgetall.side_effect = [
        {"1": "5", "2": "3"},   # alice
        {"1": "4", "3": "2"}    # bob
    ]

    response = client.get("/api/recommend/alice")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)

def test_recommend_unknown_user(client):
    from recommender_service import r
    r.keys.return_value = ["ratings:bob"]
    r.hgetall.return_value = {"1": "4"}

    response = client.get("/api/recommend/unknown")

    assert response.status_code == 200
    assert response.get_json() == {}

def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"http_requests_total" in response.data