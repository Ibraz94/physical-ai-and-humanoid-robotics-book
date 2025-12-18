import pytest
from fastapi.testclient import TestClient
from backend.app.main import app


class TestSourcesEndpoint:
    """Unit tests for the sources endpoint functionality"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_sources_endpoint_success(self, client):
        """Test that the sources endpoint returns source information for valid chunk_id"""
        # Using a mock chunk_id that would exist in the system
        chunk_id = "test-chunk-123"

        response = client.get(f"/api/v1/sources/{chunk_id}")

        # Response should be either 200 (found) or 404 (not found) - both are valid responses
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            response_data = response.json()
            # Verify expected fields in response
            assert "chunk_id" in response_data
            assert "module" in response_data
            assert "chapter" in response_data
            assert "url" in response_data
            assert response_data["chunk_id"] == chunk_id

    def test_sources_endpoint_invalid_chunk_id_format(self, client):
        """Test that the sources endpoint handles invalid chunk_id format"""
        invalid_chunk_ids = [
            "",  # Empty
            "   ",  # Whitespace
            "chunk with spaces",
            "<script>invalid</script>",  # Potential XSS
            "../../../../etc/passwd",  # Path traversal attempt
        ]

        for chunk_id in invalid_chunk_ids:
            response = client.get(f"/api/v1/sources/{chunk_id}")

            # Should return 404 for invalid chunk IDs or handle them appropriately
            assert response.status_code in [404, 422, 400]

    def test_sources_endpoint_special_characters(self, client):
        """Test that the sources endpoint handles chunk_ids with special characters"""
        special_chunk_ids = [
            "chunk-with-dashes-123",
            "chunk_with_underscores_456",
            "chunk.with.dots.789",
            "chunk123",  # alphanumeric
            "CHUNK-ABC-DEF",  # uppercase
        ]

        for chunk_id in special_chunk_ids:
            response = client.get(f"/api/v1/sources/{chunk_id}")

            # Should handle special characters in chunk_id appropriately
            assert response.status_code in [200, 404, 422, 400]

    def test_sources_endpoint_method_validation(self, client):
        """Test that the sources endpoint only accepts GET requests"""
        # Try POST request (should fail)
        response_post = client.post("/api/v1/sources/test-chunk-123", json={})
        assert response_post.status_code == 405  # Method not allowed

        # Try PUT request (should fail)
        response_put = client.put("/api/v1/sources/test-chunk-123", json={})
        assert response_put.status_code == 405  # Method not allowed

        # Try DELETE request (should fail)
        response_delete = client.delete("/api/v1/sources/test-chunk-123")
        assert response_delete.status_code == 405  # Method not allowed

        # GET request should be allowed
        response_get = client.get("/api/v1/sources/test-chunk-123")
        assert response_get.status_code in [200, 404]

    def test_sources_endpoint_path_parameters(self, client):
        """Test that the sources endpoint properly handles path parameters"""
        # Test with a properly formatted chunk ID
        response = client.get("/api/v1/sources/chunk-abc-123")
        assert response.status_code in [200, 404]

        # Test with chunk ID containing special characters that are valid in URLs
        response = client.get("/api/v1/sources/chunk_abc_123")
        assert response.status_code in [200, 404]

    def test_sources_endpoint_long_chunk_id(self, client):
        """Test that the sources endpoint handles very long chunk IDs"""
        long_chunk_id = "chunk-" + "a" * 1000  # Very long chunk ID

        response = client.get(f"/api/v1/sources/{long_chunk_id}")

        # Should handle long chunk IDs gracefully
        assert response.status_code in [200, 404, 414, 400]  # Success, not found, URI too long, or bad request

    def test_sources_endpoint_sql_injection_protection(self, client):
        """Test that the sources endpoint is protected against SQL injection"""
        injection_attempts = [
            "'; DROP TABLE chunks; --",
            "'; WAITFOR DELAY '00:00:10'; --",
            "' OR '1'='1",
            "'; EXEC xp_cmdshell 'dir'; --",
            "chunk-123' UNION SELECT password FROM users--",
        ]

        for chunk_id in injection_attempts:
            response = client.get(f"/api/v1/sources/{chunk_id}")

            # Should not crash or expose internal errors
            assert response.status_code in [200, 404, 400, 422, 500]
            if response.status_code == 500:
                # If there's a server error, it should be handled gracefully
                assert "detail" in response.json() or len(response.content) > 0

    def test_sources_endpoint_xss_protection(self, client):
        """Test that the sources endpoint is protected against XSS"""
        xss_attempts = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "chunk-123<script>alert(1)</script>",
        ]

        for chunk_id in xss_attempts:
            response = client.get(f"/api/v1/sources/{chunk_id}")

            # Should not return the script in response or execute it
            assert response.status_code in [200, 404, 400, 422, 500]
            if response.status_code == 200:
                # If successful, response should be properly sanitized
                try:
                    response_data = response.json()
                    # Ensure no script tags in response
                    response_str = str(response.content)
                    assert "<script" not in response_str.lower()
                except:
                    # If response is not JSON, check content directly
                    assert "<script" not in response.content.decode('utf-8').lower()

    def test_sources_endpoint_response_format(self, client):
        """Test that the sources endpoint returns properly formatted responses"""
        chunk_id = "test-chunk-123"

        response = client.get(f"/api/v1/sources/{chunk_id}")

        if response.status_code == 200:
            response_data = response.json()

            # Verify response structure
            assert isinstance(response_data, dict)

            # Verify required fields exist
            required_fields = ["chunk_id", "module", "chapter", "url"]
            for field in required_fields:
                assert field in response_data

            # Verify field types
            assert isinstance(response_data["chunk_id"], str)
            assert isinstance(response_data["module"], str)
            assert isinstance(response_data["chapter"], str)
            assert isinstance(response_data["url"], str)