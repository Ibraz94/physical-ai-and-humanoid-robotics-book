import pytest
from fastapi.testclient import TestClient
from backend.app.main import app


class TestSelectAPIValidation:
    """API validation tests for the /select endpoint"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_select_text_field_validation(self, client):
        """Test validation for the text field in select endpoint"""
        # Test with empty text
        response = client.post("/api/v1/select", json={"text": "", "source_url": "https://example.com"})
        assert response.status_code == 422

        # Test with whitespace-only text
        response = client.post("/api/v1/select", json={"text": "   ", "source_url": "https://example.com"})
        assert response.status_code == 422

        # Test with text that's too long (if there's a limit)
        long_text = "A" * 10000  # 10,000 character text
        response = client.post("/api/v1/select", json={"text": long_text, "source_url": "https://example.com"})
        # Should handle gracefully
        assert response.status_code in [200, 201, 413, 422]

        # Test with valid text
        response = client.post("/api/v1/select",
                              json={"text": "This is valid selected text", "source_url": "https://example.com"})
        assert response.status_code in [200, 201]

    def test_select_source_url_field_validation(self, client):
        """Test validation for the source_url field in select endpoint"""
        # Test with empty source_url
        response = client.post("/api/v1/select", json={"text": "valid text", "source_url": ""})
        assert response.status_code == 422

        # Test with invalid URL format
        response = client.post("/api/v1/select",
                              json={"text": "valid text", "source_url": "not-a-valid-url"})
        # May return validation error or accept it depending on implementation
        assert response.status_code in [200, 201, 422]

        # Test with valid URL
        response = client.post("/api/v1/select",
                              json={"text": "valid text", "source_url": "https://example.com/page"})
        assert response.status_code in [200, 201]

    def test_select_field_type_validation(self, client):
        """Test type validation for fields in select endpoint"""
        # Test text as non-string
        response = client.post("/api/v1/select",
                              json={"text": 12345, "source_url": "https://example.com"})
        assert response.status_code == 422

        # Test source_url as non-string
        response = client.post("/api/v1/select",
                              json={"text": "valid text", "source_url": 12345})
        assert response.status_code == 422

        # Test with arrays
        response = client.post("/api/v1/select",
                              json={"text": ["text"], "source_url": ["url"]})
        assert response.status_code == 422

        # Test with objects
        response = client.post("/api/v1/select",
                              json={"text": {"text": "value"}, "source_url": {"url": "value"}})
        assert response.status_code == 422

    def test_select_required_fields_validation(self, client):
        """Test required fields validation for select endpoint"""
        # Test with no fields
        response = client.post("/api/v1/select", json={})
        assert response.status_code == 422

        # Test with only text field
        response = client.post("/api/v1/select", json={"text": "valid text"})
        assert response.status_code == 422

        # Test with only source_url field
        response = client.post("/api/v1/select", json={"source_url": "https://example.com"})
        assert response.status_code == 422

        # Test with both required fields
        response = client.post("/api/v1/select",
                              json={"text": "valid text", "source_url": "https://example.com"})
        assert response.status_code in [200, 201]


class TestSourcesAPIValidation:
    """API validation tests for the /sources endpoint"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_sources_chunk_id_validation(self, client):
        """Test validation for chunk_id path parameter in sources endpoint"""
        # Test with empty chunk_id (this may result in 404 or 405 depending on routing)
        response = client.get("/api/v1/sources/")
        assert response.status_code in [404, 405]

        # Test with special characters that could be malicious
        malicious_ids = [
            "../../../etc/passwd",  # Path traversal
            "<script>alert('xss')</script>",  # XSS attempt
            "'; DROP TABLE chunks; --",  # SQL injection
            "javascript:alert('xss')",  # JavaScript attempt
            "chunk%00null",  # Null byte injection
        ]

        for malicious_id in malicious_ids:
            response = client.get(f"/api/v1/sources/{malicious_id}")
            # Should not crash or expose internal errors
            assert response.status_code in [404, 400, 422, 500]

    def test_sources_chunk_id_format_validation(self, client):
        """Test format validation for chunk_id in sources endpoint"""
        # Test with various valid formats
        valid_formats = [
            "chunk-123",
            "chunk_123_456",
            "chunk.123.456",
            "CHUNK-ABC-DEF",
            "chunk123abc",
            "chunk-123-abc-def",
        ]

        for chunk_id in valid_formats:
            response = client.get(f"/api/v1/sources/{chunk_id}")
            # Should handle valid formats gracefully (either found or not found)
            assert response.status_code in [200, 404]

    def test_sources_chunk_id_length_validation(self, client):
        """Test length validation for chunk_id in sources endpoint"""
        # Test with very long chunk_id
        long_chunk_id = "chunk-" + "a" * 1000  # Very long ID
        response = client.get(f"/api/v1/sources/{long_chunk_id}")
        # Should handle gracefully
        assert response.status_code in [200, 404, 414, 400]  # Success, not found, URI too long, or bad request

    def test_sources_method_validation(self, client):
        """Test HTTP method validation for sources endpoint"""
        # Test allowed method
        response_get = client.get("/api/v1/sources/test-chunk")
        assert response_get.status_code in [200, 404]  # Either found or not found

        # Test disallowed methods
        response_post = client.post("/api/v1/sources/test-chunk", json={})
        assert response_post.status_code == 405  # Method not allowed

        response_put = client.put("/api/v1/sources/test-chunk", json={})
        assert response_put.status_code == 405  # Method not allowed

        response_delete = client.delete("/api/v1/sources/test-chunk")
        assert response_delete.status_code == 405  # Method not allowed


class TestAPICommonValidation:
    """Common API validation tests for all endpoints"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_json_content_type_validation(self, client):
        """Test JSON content type validation across endpoints"""
        endpoints_to_test = [
            ("/api/v1/query", {"query": "test"}),
            ("/api/v1/select", {"text": "test", "source_url": "https://example.com"}),
            ("/api/v1/ingest", {"sitemap_url": "https://example.com/sitemap.xml"}),
        ]

        for endpoint, valid_payload in endpoints_to_test:
            # Test with proper JSON content type
            response = client.post(endpoint, json=valid_payload)
            assert response.status_code in [200, 201, 202, 400, 422]

            # Test with explicit content type header
            response = client.post(
                endpoint,
                json=valid_payload,
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code in [200, 201, 202, 400, 422]

    def test_large_payload_handling(self, client):
        """Test handling of large payloads across endpoints"""
        large_query = "A" * 50000  # 50k character query
        response = client.post("/api/v1/query", json={"query": large_query})
        assert response.status_code in [200, 413, 422, 400, 500]

        large_text = "A" * 50000  # 50k character text
        response = client.post("/api/v1/select",
                              json={"text": large_text, "source_url": "https://example.com"})
        assert response.status_code in [200, 201, 413, 422, 400, 500]

    def test_special_character_handling(self, client):
        """Test handling of special characters across endpoints"""
        special_chars_payloads = [
            {"query": "What are RAG systems? ñáéíóú 🤖"},
            {"text": "Text with special chars: ñáéíóú 🤖 \"quotes\" and 'apostrophes'", "source_url": "https://example.com"},
            {"sitemap_url": "https://example.com/sitemap-ñáéíóú.xml"},
        ]

        endpoints = ["/api/v1/query", "/api/v1/select", "/api/v1/ingest"]

        for i, payload in enumerate(special_chars_payloads):
            response = client.post(endpoints[i], json=payload)
            assert response.status_code in [200, 201, 202, 400, 422]

    def test_security_validation_across_endpoints(self, client):
        """Test common security validations across all endpoints"""
        # Test SQL injection attempts
        sql_injection_attempts = [
            {"query": "'; DROP TABLE users; --"},
            {"text": "'; DROP TABLE users; --", "source_url": "https://example.com"},
            {"sitemap_url": "'; DROP TABLE users; --"},
        ]

        endpoints = ["/api/v1/query", "/api/v1/select", "/api/v1/ingest"]

        for i, payload in enumerate(sql_injection_attempts):
            response = client.post(endpoints[i], json=payload)
            # Should not crash or expose internal errors
            assert response.status_code in [200, 400, 422, 500]

        # Test XSS attempts in path parameters (for sources endpoint)
        xss_attempts = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
        ]

        for xss_attempt in xss_attempts:
            response = client.get(f"/api/v1/sources/{xss_attempt}")
            assert response.status_code in [200, 404, 400, 422, 500]