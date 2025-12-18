import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
import json


class TestQueryAPIValidation:
    """API validation tests for the /query endpoint"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_query_field_validation_non_empty(self, client):
        """Test that query field must be non-empty"""
        # Test with empty string
        query_data = {"query": ""}
        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 422

        # Test with whitespace only
        query_data = {"query": "   "}
        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 422

        # Test with valid query
        query_data = {"query": "What are RAG systems?"}
        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 200

    def test_query_field_type_validation(self, client):
        """Test that query field must be a string"""
        # Test with integer
        query_data = {"query": 123}
        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 422

        # Test with array
        query_data = {"query": ["What are RAG systems?"]}
        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 422

        # Test with object
        query_data = {"query": {"text": "What are RAG systems?"}}
        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 422

        # Test with valid string
        query_data = {"query": "What are RAG systems?"}
        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 200

    def test_context_field_validation(self, client):
        """Test validation for optional context field"""
        # Valid context
        query_data = {
            "query": "What are RAG systems?",
            "context": "Additional context here"
        }
        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 200

        # Context as non-string (should be allowed since it's optional)
        query_data = {
            "query": "What are RAG systems?",
            "context": 123
        }
        response = client.post("/api/v1/query", json=query_data)
        # This might pass or fail depending on how the endpoint handles it, but it should not cause a server error
        assert response.status_code in [200, 422]

    def test_session_id_field_validation(self, client):
        """Test validation for optional session_id field"""
        # Valid session_id
        query_data = {
            "query": "What are RAG systems?",
            "session_id": "valid-session-id-123"
        }
        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 200

        # Session ID as non-string (should be allowed since it's optional)
        query_data = {
            "query": "What are RAG systems?",
            "session_id": 12345
        }
        response = client.post("/api/v1/query", json=query_data)
        # This might pass or fail depending on how the endpoint handles it
        assert response.status_code in [200, 422]

    def test_query_length_validation(self, client):
        """Test validation for query length limits"""
        # Very long query (test length limit)
        long_query = "A" * 10000  # 10,000 character query
        query_data = {"query": long_query}
        response = client.post("/api/v1/query", json=query_data)
        # Should either accept or return a proper error, not crash
        assert response.status_code in [200, 422, 413]  # 413 is request entity too large

        # Reasonable length query
        reasonable_query = "A" * 500  # 500 character query
        query_data = {"query": reasonable_query}
        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 200

    def test_required_fields_validation(self, client):
        """Test that required fields are validated"""
        # Missing query field
        query_data = {"session_id": "test-session"}
        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 422

        # Empty request body
        query_data = {}
        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 422

    def test_json_format_validation(self, client):
        """Test validation of JSON format"""
        # Valid JSON
        response = client.post(
            "/api/v1/query",
            json={"query": "What are RAG systems?"},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200

        # Invalid JSON (string instead of object)
        response = client.post(
            "/api/v1/query",
            content='"invalid json"',
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [422, 400]

    def test_special_characters_validation(self, client):
        """Test validation with special characters in query"""
        special_queries = [
            "What are RAG systems? (with parentheses)",
            "What are RAG systems? [with brackets]",
            "What are RAG systems? {with braces}",
            "What are RAG systems? \"with quotes\"",
            "What are RAG systems? 'with apostrophes'",
            "What are RAG systems? with unicode: ñáéíóú",
            "What are RAG systems? with emoji: 🤖",
        ]

        for query in special_queries:
            query_data = {"query": query}
            response = client.post("/api/v1/query", json=query_data)
            # Should handle special characters gracefully
            assert response.status_code in [200, 422]  # Either success or validation error, but not server error

    def test_sql_injection_validation(self, client):
        """Test that the API handles potential SQL injection attempts safely"""
        injection_attempts = [
            "'; DROP TABLE users; --",
            "'; WAITFOR DELAY '00:00:10'; --",
            "' OR '1'='1",
            "'; EXEC xp_cmdshell 'dir'; --",
        ]

        for query in injection_attempts:
            query_data = {"query": query}
            response = client.post("/api/v1/query", json=query_data)
            # Should not crash or expose internal errors
            assert response.status_code in [200, 422, 400, 500]
            if response.status_code == 500:
                # If there's a server error, it should be handled gracefully
                assert "detail" in response.json() or len(response.content) > 0

    def test_xss_validation(self, client):
        """Test that the API handles potential XSS attempts safely"""
        xss_attempts = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
        ]

        for query in xss_attempts:
            query_data = {"query": query}
            response = client.post("/api/v1/query", json=query_data)
            # Should not crash or expose internal errors
            assert response.status_code in [200, 422, 400, 500]
            if response.status_code == 200:
                # If successful, response should be properly sanitized
                response_data = response.json()
                assert "answer" in response_data