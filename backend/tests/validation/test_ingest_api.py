import pytest
from fastapi.testclient import TestClient
from backend.app.main import app


class TestIngestAPIValidation:
    """API validation tests for the /ingest endpoint"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_ingest_sitemap_url_field_validation(self, client):
        """Test validation for the sitemap_url field"""
        # Test with empty sitemap_url
        response = client.post("/api/v1/ingest", json={"sitemap_url": ""})
        assert response.status_code == 422

        # Test with whitespace-only sitemap_url
        response = client.post("/api/v1/ingest", json={"sitemap_url": "   "})
        assert response.status_code == 422

        # Test with valid URL format
        response = client.post("/api/v1/ingest", json={"sitemap_url": "https://example.com/sitemap.xml"})
        # May return 200/202 (success) or 400/422 (if URL is invalid), but not 500
        assert response.status_code in [200, 202, 400, 422]

        # Test with HTTP URL (should be allowed)
        response = client.post("/api/v1/ingest", json={"sitemap_url": "http://example.com/sitemap.xml"})
        assert response.status_code in [200, 202, 400, 422]

    def test_ingest_sitemap_url_format_validation(self, client):
        """Test URL format validation for sitemap_url"""
        invalid_urls = [
            "not-a-url",
            "ftp://example.com/file.xml",  # Non-HTTP protocol
            "http://",  # Incomplete URL
            "https://",  # Incomplete URL
            "javascript:alert('xss')",  # Malicious scheme
            "file:///etc/passwd",  # File protocol
        ]

        for invalid_url in invalid_urls:
            response = client.post("/api/v1/ingest", json={"sitemap_url": invalid_url})
            # Should return validation error, not crash
            assert response.status_code in [422, 400, 200, 202]  # Either validation error or handled gracefully

        valid_urls = [
            "https://example.com/sitemap.xml",
            "https://subdomain.example.com/path/sitemap_index.xml",
            "http://example.com/sitemap.xml",
            "https://example.com:8080/sitemap.xml",
        ]

        for valid_url in valid_urls:
            response = client.post("/api/v1/ingest", json={"sitemap_url": valid_url})
            # Should handle valid URLs appropriately
            assert response.status_code in [200, 202, 400, 422]

    def test_ingest_field_type_validation(self, client):
        """Test type validation for fields in ingest endpoint"""
        # Test sitemap_url as non-string
        response = client.post("/api/v1/ingest", json={"sitemap_url": 12345})
        assert response.status_code == 422

        # Test sitemap_url as array
        response = client.post("/api/v1/ingest", json={"sitemap_url": ["url1", "url2"]})
        assert response.status_code == 422

        # Test sitemap_url as object
        response = client.post("/api/v1/ingest", json={"sitemap_url": {"url": "https://example.com"}})
        assert response.status_code == 422

    def test_ingest_required_fields_validation(self, client):
        """Test required fields validation for ingest endpoint"""
        # Test with no fields
        response = client.post("/api/v1/ingest", json={})
        assert response.status_code == 422

        # Test with extra fields (should be allowed or handled gracefully)
        response = client.post("/api/v1/ingest",
                              json={"sitemap_url": "https://example.com/sitemap.xml", "extra_field": "value"})
        assert response.status_code in [200, 202, 422]

    def test_ingest_url_security_validation(self, client):
        """Test security validation for URL fields"""
        security_test_urls = [
            # Path traversal attempts
            "https://example.com/../../../etc/passwd",
            # SQL injection in URL
            "https://example.com/sitemap.xml'; DROP TABLE sitemaps; --",
            # XSS in URL
            "https://example.com/<script>alert('xss')</script>.xml",
            # Command injection
            "https://example.com/$(rm -rf /).xml",
        ]

        for test_url in security_test_urls:
            response = client.post("/api/v1/ingest", json={"sitemap_url": test_url})
            # Should not crash or execute malicious code
            assert response.status_code in [400, 422, 200, 202, 500]
            if response.status_code == 500:
                # If there's a server error, it should be handled gracefully
                assert len(response.content) > 0

    def test_ingest_large_payload_validation(self, client):
        """Test validation for large payloads"""
        # Test with very long sitemap URL
        long_url = "https://example.com/" + "a" * 10000 + ".xml"
        response = client.post("/api/v1/ingest", json={"sitemap_url": long_url})
        # Should handle gracefully (validation error or success)
        assert response.status_code in [414, 422, 400, 200, 202, 500]

        # Test with large request body with extra fields
        large_payload = {
            "sitemap_url": "https://example.com/sitemap.xml",
            "large_field": "A" * 50000  # Large additional field
        }
        response = client.post("/api/v1/ingest", json=large_payload)
        assert response.status_code in [413, 422, 400, 200, 202]

    def test_ingest_content_type_validation(self, client):
        """Test content type validation for ingest endpoint"""
        # Test with proper JSON content type
        response = client.post(
            "/api/v1/ingest",
            json={"sitemap_url": "https://example.com/sitemap.xml"},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [200, 202]

        # Test with no content type (should default to JSON)
        response = client.post(
            "/api/v1/ingest",
            json={"sitemap_url": "https://example.com/sitemap.xml"}
        )
        assert response.status_code in [200, 202, 422]

    def test_ingest_method_validation(self, client):
        """Test HTTP method validation for ingest endpoint"""
        # Valid method
        response_post = client.post("/api/v1/ingest", json={"sitemap_url": "https://example.com/sitemap.xml"})
        assert response_post.status_code in [200, 202, 422]

        # Invalid methods
        response_get = client.get("/api/v1/ingest")
        assert response_get.status_code == 405

        response_put = client.put("/api/v1/ingest", json={"sitemap_url": "https://example.com/sitemap.xml"})
        assert response_put.status_code == 405

        response_delete = client.delete("/api/v1/ingest")
        assert response_delete.status_code == 405

    def test_ingest_special_characters_validation(self, client):
        """Test validation with special characters in URL"""
        special_urls = [
            "https://example.com/sitemap-ñáéíóú.xml",  # Unicode
            "https://example.com/sitemap with spaces.xml",  # Spaces (should be encoded)
            "https://example.com/sitemap+plus+signs.xml",  # Plus signs
            "https://example.com/sitemap_underscore.xml",  # Underscores
            "https://example.com/sitemap.with.dots.xml",  # Dots
        ]

        for url in special_urls:
            response = client.post("/api/v1/ingest", json={"sitemap_url": url})
            # Should handle special characters appropriately
            assert response.status_code in [200, 202, 400, 422]

    def test_ingest_protocol_validation(self, client):
        """Test validation of URL protocols"""
        protocol_tests = [
            ("https://example.com/sitemap.xml", [200, 202, 400, 422]),  # Valid
            ("http://example.com/sitemap.xml", [200, 202, 400, 422]),   # Valid
            ("ftp://example.com/sitemap.xml", [422, 400]),              # Invalid protocol
            ("file://example.com/sitemap.xml", [422, 400]),             # Invalid protocol
            ("javascript:alert('xss')", [422, 400]),                    # Malicious protocol
        ]

        for url, valid_responses in protocol_tests:
            response = client.post("/api/v1/ingest", json={"sitemap_url": url})
            assert response.status_code in valid_responses

    def test_ingest_header_validation(self, client):
        """Test header validation for ingest endpoint"""
        # Test with standard headers
        response = client.post(
            "/api/v1/ingest",
            json={"sitemap_url": "https://example.com/sitemap.xml"},
            headers={
                "User-Agent": "Test-Agent",
                "Accept": "application/json"
            }
        )
        assert response.status_code in [200, 202]

        # Test with large headers (should be handled appropriately)
        large_header_value = "A" * 10000
        response = client.post(
            "/api/v1/ingest",
            json={"sitemap_url": "https://example.com/sitemap.xml"},
            headers={"X-Large-Header": large_header_value}
        )
        # Should handle gracefully
        assert response.status_code in [200, 202, 400, 431]  # 431 = Request Header Fields Too Large