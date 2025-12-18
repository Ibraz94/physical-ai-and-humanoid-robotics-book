import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models.query import QueryRequest
import json


class TestQueryEndpointIntegration:
    """Integration tests for the query endpoint"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_query_endpoint_success(self, client):
        """Test that the query endpoint returns a successful response"""
        query_data = {
            "query": "What are the key principles of RAG systems?",
            "session_id": "test_session_123"
        }

        response = client.post("/api/v1/query", json=query_data)

        assert response.status_code == 200
        response_data = response.json()
        assert "answer" in response_data
        assert "citations" in response_data
        assert isinstance(response_data["citations"], list)

    def test_query_endpoint_with_context(self, client):
        """Test that the query endpoint handles queries with additional context"""
        query_data = {
            "query": "Explain the concept?",
            "context": "This is additional context about the concept",
            "session_id": "test_session_456"
        }

        response = client.post("/api/v1/query", json=query_data)

        assert response.status_code == 200
        response_data = response.json()
        assert "answer" in response_data
        assert "citations" in response_data

    def test_query_endpoint_missing_query(self, client):
        """Test that the query endpoint handles missing query field"""
        query_data = {
            "session_id": "test_session_789"
        }

        response = client.post("/api/v1/query", json=query_data)

        assert response.status_code == 422  # Validation error

    def test_query_endpoint_empty_query(self, client):
        """Test that the query endpoint handles empty query"""
        query_data = {
            "query": "",
            "session_id": "test_session_000"
        }

        response = client.post("/api/v1/query", json=query_data)

        assert response.status_code == 422  # Validation error

    def test_query_endpoint_insufficient_context_response(self, client):
        """Test that the query endpoint can return 'I don't know' response"""
        query_data = {
            "query": "What is the meaning of life according to the book?",
            "session_id": "test_session_abc"
        }

        response = client.post("/api/v1/query", json=query_data)

        # Response should be successful, but may contain "I don't know" if no relevant context found
        assert response.status_code == 200
        response_data = response.json()
        assert "answer" in response_data
        assert "citations" in response_data

    def test_query_endpoint_session_tracking(self, client):
        """Test that the query endpoint properly handles session tracking"""
        query_data = {
            "query": "What was my previous question?",
            "session_id": "persistent_session_123"
        }

        response = client.post("/api/v1/query", json=query_data)

        assert response.status_code == 200
        response_data = response.json()
        assert "session_id" in response_data
        assert response_data["session_id"] == "persistent_session_123"