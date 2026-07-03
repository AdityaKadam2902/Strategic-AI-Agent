"""
Integration tests for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class TestHealthEndpoint:
    """Test cases for health check endpoint."""

    def test_health_check(self):
        """Test health check returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "environment" in data


class TestDebateEndpoint:
    """Test cases for debate analysis endpoint."""

    def test_debate_request_validation(self):
        """Test debate request validation."""
        response = client.post("/api/v1/debate", json={
            "decision": "Short?"
        })
        assert response.status_code == 422

    def test_debate_request_missing_field(self):
        """Test debate request requires decision field."""
        response = client.post("/api/v1/debate", json={})
        assert response.status_code == 422
