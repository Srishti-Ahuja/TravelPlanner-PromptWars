import pytest
from unittest.mock import MagicMock, patch
import sys

# Mock google libraries before importing app to avoid initialization errors
mock_genai = MagicMock()
sys.modules["google.generativeai"] = mock_genai
sys.modules["google.cloud.secretmanager"] = MagicMock()
sys.modules["google.cloud.logging"] = MagicMock()
sys.modules["google.cloud.monitoring"] = MagicMock()
sys.modules["google.cloud.monitoring_v3"] = MagicMock()
sys.modules["googlemaps"] = MagicMock()

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@patch("backend.services.gemini_service.GeminiService.parse_trip_intent")
def test_extract_intent(mock_gemini):
    # Mock data
    mock_gemini.return_value = {
        "intent": "Visit Tokyo",
        "cities": ["Tokyo"],
        "markers": [{"name": "Shibuya", "lat": 35.6, "lng": 139.7, "description": "Tech hub", "type": "attraction"}]
    }
    
    response = client.post("/api/intent", json={"query": "Go to Tokyo"})
    assert response.status_code == 200
    assert response.json()["intent"] == "Visit Tokyo"
    assert len(response.json()["markers"]) == 1

@patch("backend.services.maps_service.MapsService.get_optimized_itinerary")
def test_generate_itinerary(mock_maps):
    mock_maps.return_value = {
        "steps": [{"instruction": "Go left", "distance": "1km", "duration": "5m"}],
        "total_distance": "1km",
        "total_duration": "5m",
        "map_polyline": "abc"
    }
    
    response = client.post("/api/itinerary", json={"points": ["A", "B"]})
    assert response.status_code == 200
    assert response.json()["total_distance"] == "1km"
