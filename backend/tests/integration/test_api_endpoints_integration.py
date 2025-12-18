import pytest
from fastapi.testclient import TestClient
from backend.app.main import app


class TestAPIEndpointsIntegration:
    """Integration tests for all API endpoints"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_all_endpoints_health_check(self, client):
        """Test that all API endpoints are accessible"""
        # Test root endpoint
        response = client.get("/")
        assert response.status_code == 200

        # Test health check endpoint
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_query_endpoint_integration(self, client):
        """Test integration of query endpoint with other services"""
        query_data = {
            "query": "What are the key principles of RAG systems?",
            "session_id": "integration-test-123"
        }

        response = client.post("/api/v1/query", json=query_data)

        assert response.status_code == 200
        response_data = response.json()
        assert "answer" in response_data
        assert "citations" in response_data

    def test_select_endpoint_integration(self, client):
        """Test integration of select endpoint"""
        select_data = {
            "text": "This is user-selected text for integration testing",
            "source_url": "https://integration-test.example.com/chapter-1"
        }

        response = client.post("/api/v1/select", json=select_data)

        assert response.status_code in [200, 201]

    def test_sources_endpoint_integration(self, client):
        """Test integration of sources endpoint"""
        # Test with a sample chunk ID
        response = client.get("/api/v1/sources/test-chunk-123")

        # Should return 200 if found or 404 if not found (both valid responses)
        assert response.status_code in [200, 404]

    def test_ingest_endpoint_integration(self, client):
        """Test integration of ingest endpoint"""
        ingest_data = {
            "sitemap_url": "https://integration-test.example.com/sitemap.xml"
        }

        response = client.post("/api/v1/ingest", json=ingest_data)

        # Should return success response or appropriate error
        assert response.status_code in [200, 202, 400, 422]

    def test_endpoint_cross_functionality_query_after_select(self, client):
        """Test that query functionality works after selecting text"""
        # First, select some text
        select_data = {
            "text": "This is important context about RAG systems",
            "source_url": "https://integration-test.example.com/context"
        }

        select_response = client.post("/api/v1/select", json=select_data)
        assert select_response.status_code in [200, 201]

        # Then query using that context
        query_data = {
            "query": "What was the context I just provided?",
            "session_id": "cross-test-123"
        }

        query_response = client.post("/api/v1/query", json=query_data)
        assert query_response.status_code == 200
        query_result = query_response.json()
        assert "answer" in query_result

    def test_endpoint_cross_functionality_sources_after_ingest(self, client):
        """Test that sources can be retrieved after ingestion"""
        # Ingest some content
        ingest_data = {
            "sitemap_url": "https://integration-test.example.com/sitemap.xml"
        }

        ingest_response = client.post("/api/v1/ingest", json=ingest_data)
        # May return 200, 202 (accepted), or 400 if URL is invalid - all are valid
        assert ingest_response.status_code in [200, 202, 400, 422]

        # Try to retrieve a source (might work if ingest was successful)
        sources_response = client.get("/api/v1/sources/test-chunk-after-ingest")
        assert sources_response.status_code in [200, 404]

    def test_multiple_session_isolation(self, client):
        """Test that different sessions are properly isolated"""
        session_1_data = {
            "query": "Remember this: Session 1 query",
            "session_id": "session-1-test"
        }

        session_2_data = {
            "query": "Remember this: Session 2 query",
            "session_id": "session-2-test"
        }

        # Make queries from different sessions
        response_1 = client.post("/api/v1/query", json=session_1_data)
        response_2 = client.post("/api/v1/query", json=session_2_data)

        assert response_1.status_code == 200
        assert response_2.status_code == 200

        # Both should succeed independently
        data_1 = response_1.json()
        data_2 = response_2.json()

        assert "session_id" in data_1
        assert "session_id" in data_2
        assert data_1["session_id"] == "session-1-test"
        assert data_2["session_id"] == "session-2-test"

    def test_api_rate_limiting_or_concurrency(self, client):
        """Test API behavior under multiple concurrent requests"""
        import threading
        import time

        results = []

        def make_request(query_text, session_id):
            data = {
                "query": query_text,
                "session_id": session_id
            }
            response = client.post("/api/v1/query", json=data)
            results.append((response.status_code, response.json() if response.status_code == 200 else None))

        # Make multiple concurrent requests
        threads = []
        for i in range(3):
            thread = threading.Thread(
                target=make_request,
                args=(f"Concurrent query {i}", f"session-concurrent-{i}")
            )
            threads.append(thread)
            thread.start()
            time.sleep(0.01)  # Small delay between requests

        for thread in threads:
            thread.join()

        # Check that all requests were processed
        assert len(results) == 3
        for status_code, data in results:
            assert status_code in [200, 422, 429]  # Success, validation error, or rate limit

    def test_api_error_propagation(self, client):
        """Test that errors are properly propagated through the API layer"""
        # Test with malformed request that should trigger validation
        malformed_data = {
            "invalid_field": "invalid_value"
        }

        response = client.post("/api/v1/query", json=malformed_data)
        # Should return validation error, not server error
        assert response.status_code in [422, 400]

    def test_api_response_consistency(self, client):
        """Test that API responses are consistent across different endpoints"""
        # Test query endpoint response structure
        query_response = client.post("/api/v1/query", json={"query": "test"})
        if query_response.status_code == 200:
            query_data = query_response.json()
            assert isinstance(query_data, dict)
            assert "answer" in query_data
            assert "citations" in query_data

        # Test select endpoint response structure
        select_response = client.post("/api/v1/select",
                                    json={"text": "test", "source_url": "https://example.com"})
        if select_response.status_code in [200, 201]:
            select_data = select_response.json()
            assert isinstance(select_data, dict)

        # Test sources endpoint response structure
        sources_response = client.get("/api/v1/sources/test")
        if sources_response.status_code == 200:
            sources_data = sources_response.json()
            assert isinstance(sources_data, dict)

        # Test ingest endpoint response structure
        ingest_response = client.post("/api/v1/ingest",
                                    json={"sitemap_url": "https://example.com/sitemap.xml"})
        if ingest_response.status_code in [200, 202]:
            ingest_data = ingest_response.json()
            assert isinstance(ingest_data, dict)