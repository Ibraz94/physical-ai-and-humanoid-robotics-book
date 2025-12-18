import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
import json


class TestQueryContract:
    """Contract tests for the /query API endpoint"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_query_endpoint_contract_success_response(self, client):
        """Test that the query endpoint returns the expected response structure"""
        query_data = {
            "query": "What are RAG systems?",
            "session_id": "test_session_123"
        }

        response = client.post("/api/v1/query", json=query_data)

        assert response.status_code == 200

        # Verify response structure
        response_data = response.json()
        assert "answer" in response_data
        assert "citations" in response_data
        assert "session_id" in response_data

        # Verify data types
        assert isinstance(response_data["answer"], str)
        assert isinstance(response_data["citations"], list)
        assert isinstance(response_data["session_id"], str)

        # Verify citations structure if present
        for citation in response_data["citations"]:
            assert "chunk_id" in citation
            assert "module" in citation
            assert "chapter" in citation
            assert "url" in citation

    def test_query_endpoint_contract_error_response(self, client):
        """Test that the query endpoint returns expected error response structure"""
        # Send invalid request (empty query)
        query_data = {
            "query": "",
            "session_id": "test_session_456"
        }

        response = client.post("/api/v1/query", json=query_data)

        # Should return validation error
        assert response.status_code == 422

    def test_query_endpoint_contract_request_fields(self, client):
        """Test that the query endpoint accepts the expected request fields"""
        # Valid request with all optional fields
        query_data = {
            "query": "What are the key principles?",
            "context": "Additional context here",
            "session_id": "test_session_789"
        }

        response = client.post("/api/v1/query", json=query_data)

        assert response.status_code == 200

        # Valid request with only required field
        query_data_minimal = {
            "query": "What are the key principles?"
        }

        response_minimal = client.post("/api/v1/query", json=query_data_minimal)

        assert response_minimal.status_code == 200

    def test_query_endpoint_contract_method(self, client):
        """Test that the query endpoint only accepts POST requests"""
        # Try GET request (should fail)
        response_get = client.get("/api/v1/query")
        assert response_get.status_code == 405  # Method not allowed

        # Try PUT request (should fail)
        response_put = client.put("/api/v1/query", json={"query": "test"})
        assert response_put.status_code == 405  # Method not allowed

        # Try PATCH request (should fail)
        response_patch = client.patch("/api/v1/query", json={"query": "test"})
        assert response_patch.status_code == 405  # Method not allowed

    def test_query_endpoint_contract_content_type(self, client):
        """Test that the query endpoint handles content type properly"""
        # Send request with proper JSON content type
        response = client.post(
            "/api/v1/query",
            json={"query": "What are RAG systems?"},
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200

    def test_query_endpoint_contract_response_headers(self, client):
        """Test that the query endpoint returns expected response headers"""
        query_data = {
            "query": "What are RAG systems?",
            "session_id": "test_session_999"
        }

        response = client.post("/api/v1/query", json=query_data)

        assert response.status_code == 200
        # Check for common headers
        assert "content-type" in response.headers
        assert "application/json" in response.headers["content-type"]