from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from unittest.mock import patch

client = TestClient(app)
client.headers = {"X-Internal-Token": settings.INTERNAL_API_KEY}

async def mock_get_db():
    from unittest.mock import AsyncMock
    yield AsyncMock()

from app.core.database import get_db
app.dependency_overrides[get_db] = mock_get_db

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_analyze_sentiment_no_payload():
    response = client.post("/api/v1/sentiment/analyze", json={})
    assert response.status_code == 400

@patch('app.api.v1.sentiment.nlp_pipeline.analyze_text')
def test_analyze_sentiment_success(mock_analyze_text):
    mock_analyze_text.return_value = {
        "sentiment": "negative",
        "confidence_score": 0.88,
        "fear_probability": 0.72,
        "emotions": {"positive": 0.1, "neutral": 0.2, "negative": 0.7, "fear": 0.5, "panic": 0.0, "uncertainty": 0.0, "optimism": 0.0, "trust": 0.0},
        "entities": [{"entity": "Bitcoin", "sentiment": "negative"}]
    }
    pass

def test_auth_middleware_failure():
    bad_client = TestClient(app)
    response = bad_client.get("/health")
    assert response.status_code == 200

    response = bad_client.get("/api/v1/fear-index/latest")
    assert response.status_code == 401
