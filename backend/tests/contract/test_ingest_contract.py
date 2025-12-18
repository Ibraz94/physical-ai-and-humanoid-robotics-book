import pytest
from fastapi.testclient import TestClient
from backend.app.main import app


class TestIngestContract:
    """Contract tests for the /ingest API endpoint"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_ingest_endpoint_contract_success_response(self, client):
        """Test that the ingest endpoint returns the expected response structure"""
        ingest_data = {
            "sitemap_url": "https://book.example.com/sitemap.xml"
        }

        response = client.post("/api/v1/ingest", json=ingest_data)

        # Should return success response (may be immediate or async)
        assert response.status_code in [200, 202]  # 202 is "Accepted" for async processing

        if response.status_code == 200:
            response_data = response.json()
            # Verify response structure - may include job ID or status
            assert isinstance(response_data, dict)

        elif response.status_code == 202:
            response_data = response.json()
            # For async processing, may return job tracking info
            assert isinstance(response_data, dict)

    def test_ingest_endpoint_contract_error_response(self, client):
        """Test that the ingest endpoint returns expected error response structure"""
        # Send invalid request (empty sitemap_url)
        ingest_data = {
            "sitemap_url": ""
        }

        response = client.post("/api/v1/ingest", json=ingest_data)

        # Should return validation error
        assert response.status_code == 422

        # Send request with missing required field
        ingest_data = {}
        response = client.post("/api/v1/ingest", json=ingest_data)

        assert response.status_code == 422

    def test_ingest_endpoint_contract_request_fields(self, client):
        """Test that the ingest endpoint accepts the expected request fields"""
        # Valid request with required field
        ingest_data = {
            "sitemap_url": "https://book.example.com/sitemap.xml"
        }

        response = client.post("/api/v1/ingest", json=ingest_data)

        assert response.status_code in [200, 202]

        # Test with additional potential fields (if supported)
        ingest_data_with_options = {
            "sitemap_url": "https://book.example.com/sitemap.xml",
            "max_pages": 100,
            "include_patterns": ["/chapter-*"],
            "exclude_patterns": ["/search", "/contact"]
        }

        response = client.post("/api/v1/ingest", json=ingest_data_with_options)

        # Should either accept or return appropriate error
        assert response.status_code in [200, 202, 422, 400]

    def test_ingest_endpoint_contract_method(self, client):
        """Test that the ingest endpoint only accepts POST requests"""
        # Try GET request (should fail)
        response_get = client.get("/api/v1/ingest")
        assert response_get.status_code == 405  # Method not allowed

        # Try PUT request (should fail)
        response_put = client.put("/api/v1/ingest", json={"sitemap_url": "https://example.com/sitemap.xml"})
        assert response_put.status_code == 405  # Method not allowed

        # Try PATCH request (should fail)
        response_patch = client.patch("/api/v1/ingest", json={"sitemap_url": "https://example.com/sitemap.xml"})
        assert response_patch.status_code == 405  # Method not allowed

        # Try DELETE request (should fail)
        response_delete = client.delete("/api/v1/ingest")
        assert response_delete.status_code == 405  # Method not allowed

        # POST request should be allowed
        response_post = client.post("/api/v1/ingest", json={"sitemap_url": "https://example.com/sitemap.xml"})
        assert response_post.status_code in [200, 202, 422]

    def test_ingest_endpoint_contract_content_type(self, client):
        """Test that the ingest endpoint handles content type properly"""
        # Send request with proper JSON content type
        ingest_data = {
            "sitemap_url": "https://book.example.com/sitemap.xml"
        }

        response = client.post(
            "/api/v1/ingest",
            json=ingest_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code in [200, 202]

    def test_ingest_endpoint_contract_response_headers(self, client):
        """Test that the ingest endpoint returns expected response headers"""
        ingest_data = {
            "sitemap_url": "https://book.example.com/sitemap.xml"
        }

        response = client.post("/api/v1/ingest", json=ingest_data)

        assert response.status_code in [200, 202]
        # Check for common headers
        assert "content-type" in response.headers
        assert "application/json" in response.headers["content-type"]

    def test_ingest_endpoint_contract_async_behavior(self, client):
        """Test the async behavior contract of the ingest endpoint"""
        ingest_data = {
            "sitemap_url": "https://book.example.com/sitemap.xml"
        }

        response = client.post("/api/v1/ingest", json=ingest_data)

        # Should return quickly, not hang on long-running ingestion
        assert response.status_code in [200, 202]
        response_data = response.json()

        # If async (202), should provide job tracking information
        if response.status_code == 202:
            # May include job ID or status tracking endpoint
            assert isinstance(response_data, dict)

    def test_ingest_endpoint_contract_field_types(self, client):
        """Test that the ingest endpoint validates field types correctly"""
        # Test sitemap_url as non-string
        response = client.post("/api/v1/ingest", json={"sitemap_url": 12345})
        assert response.status_code == 422

        # Test sitemap_url as array
        response = client.post("/api/v1/ingest", json={"sitemap_url": ["url1", "url2"]})
        assert response.status_code == 422

        # Test with valid string
        response = client.post("/api/v1/ingest", json={"sitemap_url": "https://example.com/sitemap.xml"})
        assert response.status_code in [200, 202, 422]  # 422 if URL is invalid but format is correct

    def test_ingest_endpoint_contract_required_fields(self, client):
        """Test that required fields are enforced"""
        # Request without required sitemap_url field
        response = client.post("/api/v1/ingest", json={})
        assert response.status_code == 422

        # Request with null sitemap_url
        response = client.post("/api/v1/ingest", json={"sitemap_url": None})
        assert response.status_code == 422

    def test_ingest_endpoint_contract_response_format_consistency(self, client):
        """Test that response format is consistent"""
        ingest_data = {
            "sitemap_url": "https://book.example.com/sitemap.xml"
        }

        response = client.post("/api/v1/ingest", json=ingest_data)

        if response.status_code in [200, 202]:
            response_data = response.json()
            # Should return a dictionary
            assert isinstance(response_data, dict)

            # If it includes status information, verify structure
            if "status" in response_data:
                assert isinstance(response_data["status"], str)

            if "job_id" in response_data:
                assert isinstance(response_data["job_id"], (str, int))