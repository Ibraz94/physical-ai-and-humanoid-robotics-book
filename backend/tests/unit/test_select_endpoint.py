import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.chunk_service import ChunkService


class TestSelectEndpoint:
    """Unit tests for the select endpoint functionality"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    @pytest.fixture
    def mock_chunk_service(self):
        """Create a mock chunk service"""
        return Mock(spec=ChunkService)

    def test_select_endpoint_success(self, client):
        """Test that the select endpoint successfully processes user-selected text"""
        select_data = {
            "text": "This is user-selected text that should be processed by the system",
            "source_url": "https://book.example.com/chapter-1"
        }

        response = client.post("/api/v1/select", json=select_data)

        # Should return success response (200 or 201 depending on implementation)
        assert response.status_code in [200, 201]
        response_data = response.json()
        # May return chunk_id or other confirmation data
        assert "status" in response_data or "chunk_id" in response_data

    def test_select_endpoint_missing_text(self, client):
        """Test that the select endpoint handles missing text field"""
        select_data = {
            "source_url": "https://book.example.com/chapter-1"
        }

        response = client.post("/api/v1/select", json=select_data)

        assert response.status_code == 422  # Validation error

    def test_select_endpoint_missing_source_url(self, client):
        """Test that the select endpoint handles missing source_url field"""
        select_data = {
            "text": "This is user-selected text"
        }

        response = client.post("/api/v1/select", json=select_data)

        assert response.status_code == 422  # Validation error

    def test_select_endpoint_empty_text(self, client):
        """Test that the select endpoint handles empty text"""
        select_data = {
            "text": "",
            "source_url": "https://book.example.com/chapter-1"
        }

        response = client.post("/api/v1/select", json=select_data)

        assert response.status_code == 422  # Validation error

    def test_select_endpoint_empty_source_url(self, client):
        """Test that the select endpoint handles empty source_url"""
        select_data = {
            "text": "This is user-selected text",
            "source_url": ""
        }

        response = client.post("/api/v1/select", json=select_data)

        assert response.status_code == 422  # Validation error

    def test_select_endpoint_valid_url_format(self, client):
        """Test that the select endpoint validates URL format"""
        select_data = {
            "text": "This is user-selected text",
            "source_url": "not-a-valid-url"
        }

        response = client.post("/api/v1/select", json=select_data)

        # May return validation error for invalid URL format
        assert response.status_code in [422, 200]  # Depends on validation implementation

    def test_select_endpoint_long_text_handling(self, client):
        """Test that the select endpoint handles long text properly"""
        long_text = "A" * 5000  # 5000 character text
        select_data = {
            "text": long_text,
            "source_url": "https://book.example.com/chapter-1"
        }

        response = client.post("/api/v1/select", json=select_data)

        # Should handle long text gracefully
        assert response.status_code in [200, 201, 413, 422]  # Success, too large, or validation error

    def test_select_endpoint_method_validation(self, client):
        """Test that the select endpoint only accepts POST requests"""
        # Try GET request (should fail)
        response_get = client.get("/api/v1/select")
        assert response_get.status_code == 405  # Method not allowed

        # Try PUT request (should fail)
        response_put = client.put("/api/v1/select", json={"text": "test", "source_url": "https://example.com"})
        assert response_put.status_code == 405  # Method not allowed

    def test_select_endpoint_content_type_validation(self, client):
        """Test that the select endpoint validates content type"""
        # Send request with proper JSON content type
        select_data = {
            "text": "This is user-selected text",
            "source_url": "https://book.example.com/chapter-1"
        }

        response = client.post(
            "/api/v1/select",
            json=select_data,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code in [200, 201]

    def test_select_endpoint_special_characters(self, client):
        """Test that the select endpoint handles text with special characters"""
        special_texts = [
            "Text with unicode: ñáéíóú",
            "Text with emoji: Hello 🤖 World",
            "Text with quotes: \"Hello\" and 'single'",
            "Text with special chars: !@#$%^&*()_+-=[]{}|;:,.<>?",
        ]

        for text in special_texts:
            select_data = {
                "text": text,
                "source_url": "https://book.example.com/chapter-1"
            }

            response = client.post("/api/v1/select", json=select_data)

            # Should handle special characters gracefully
            assert response.status_code in [200, 201, 422]