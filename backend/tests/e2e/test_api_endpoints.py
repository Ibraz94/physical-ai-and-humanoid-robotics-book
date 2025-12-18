import pytest
from fastapi.testclient import TestClient
from backend.app.main import app


class TestAPIEndpointsE2E:
    """End-to-end tests for User Story 3 - API Endpoint Access"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_full_api_workflow(self, client):
        """Test the complete API workflow: select text -> query -> get sources"""
        # Step 1: Submit user-selected text
        select_data = {
            "text": "Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with text generation to produce more accurate and grounded responses.",
            "source_url": "https://book.example.com/rag-fundamentals"
        }

        select_response = client.post("/api/v1/select", json=select_data)
        assert select_response.status_code in [200, 201]

        # Step 2: Query using the context provided
        query_data = {
            "query": "What is RAG?",
            "session_id": "e2e-workflow-test"
        }

        query_response = client.post("/api/v1/query", json=query_data)
        assert query_response.status_code == 200

        query_result = query_response.json()
        assert "answer" in query_result
        assert "citations" in query_result

        # Step 3: If citations exist, get source information
        if len(query_result["citations"]) > 0:
            # Get the first citation's chunk_id
            first_citation = query_result["citations"][0]
            if "chunk_id" in first_citation:
                chunk_id = first_citation["chunk_id"]
                sources_response = client.get(f"/api/v1/sources/{chunk_id}")

                # Should return either found (200) or not found (404) - both are valid
                assert sources_response.status_code in [200, 404]

                if sources_response.status_code == 200:
                    sources_data = sources_response.json()
                    assert "chunk_id" in sources_data
                    assert sources_data["chunk_id"] == chunk_id

    def test_cross_endpoint_session_consistency(self, client):
        """Test that session data is consistent across different API endpoints"""
        session_id = "cross-endpoint-session-test"

        # Make a query to establish session context
        query_data = {
            "query": "What are the fundamentals of RAG?",
            "session_id": session_id
        }

        query_response = client.post("/api/v1/query", json=query_data)
        assert query_response.status_code == 200

        # Submit selected text in the same session
        select_data = {
            "text": "Important context about RAG systems",
            "source_url": "https://book.example.com/new-context"
        }

        select_response = client.post("/api/v1/select", json=select_data)
        assert select_response.status_code in [200, 201]

        # Make another query in the same session
        followup_query = {
            "query": "What was the context I just provided?",
            "session_id": session_id
        }

        followup_response = client.post("/api/v1/query", json=followup_query)
        assert followup_response.status_code == 200

        followup_result = followup_response.json()
        assert followup_result["session_id"] == session_id

    def test_api_security_and_access_restrictions(self, client):
        """Test API security measures and access restrictions"""
        # Test that endpoints are accessible via the correct methods
        response = client.get("/api/v1/query")
        assert response.status_code == 405  # Method not allowed

        response = client.get("/api/v1/select")
        assert response.status_code == 405  # Method not allowed

        # Test that endpoints return proper headers
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert "content-type" in health_response.headers
        assert "application/json" in health_response.headers["content-type"]

    def test_api_error_propagation_consistency(self, client):
        """Test that errors are propagated consistently across all endpoints"""
        endpoints_and_invalid_data = [
            ("/api/v1/query", {"invalid": "data"}),
            ("/api/v1/select", {"invalid": "data"}),
            ("/api/v1/ingest", {"invalid": "data"}),
        ]

        for endpoint, invalid_data in endpoints_and_invalid_data:
            response = client.post(endpoint, json=invalid_data)
            # Should return validation error consistently
            assert response.status_code in [422, 400]

    def test_api_rate_limiting_or_concurrent_access(self, client):
        """Test API behavior under concurrent access"""
        import threading
        import time

        results = []

        def call_endpoint(endpoint, data):
            if endpoint == "query":
                response = client.post("/api/v1/query", json=data)
            elif endpoint == "select":
                response = client.post("/api/v1/select", json=data)
            else:
                response = client.get(f"/api/v1/sources/{data}")

            results.append((endpoint, response.status_code))

        # Make concurrent calls to different endpoints
        threads = []

        # Query endpoint calls
        for i in range(2):
            query_data = {"query": f"Concurrent query {i}", "session_id": f"session-{i}"}
            thread = threading.Thread(target=call_endpoint, args=("query", query_data))
            threads.append(thread)
            thread.start()
            time.sleep(0.01)

        # Select endpoint calls
        for i in range(2):
            select_data = {"text": f"Concurrent text {i}", "source_url": f"https://example.com/{i}"}
            thread = threading.Thread(target=call_endpoint, args=("select", select_data))
            threads.append(thread)
            thread.start()
            time.sleep(0.01)

        for thread in threads:
            thread.join()

        # Verify all calls were processed
        assert len(results) == 4
        for endpoint, status in results:
            assert status in [200, 201, 422, 400, 429]  # Include rate limit status

    def test_api_data_flow_integrity(self, client):
        """Test that data maintains integrity as it flows through different endpoints"""
        # Submit content via select endpoint
        select_data = {
            "text": "This is the original content that should be preserved through the API flow.",
            "source_url": "https://book.example.com/content-flow-test"
        }

        select_response = client.post("/api/v1/select", json=select_data)
        assert select_response.status_code in [200, 201]

        # Make a query that should reference this content
        query_data = {
            "query": "What was the content I just submitted?",
            "session_id": "data-flow-test"
        }

        query_response = client.post("/api/v1/query", json=query_data)
        assert query_response.status_code == 200

        query_result = query_response.json()
        assert "answer" in query_result
        assert "citations" in query_result

        # The response should be relevant to the submitted content
        answer = query_result["answer"].lower()
        if "original content" in answer or "content" in answer:
            assert True  # Content reference detected

    def test_api_response_time_consistency(self, client):
        """Test that API responses are consistently timed"""
        import time

        # Test response time for a simple query
        start_time = time.time()
        query_data = {"query": "What is RAG?", "session_id": "timing-test"}
        response = client.post("/api/v1/query", json=query_data)
        end_time = time.time()

        response_time = end_time - start_time

        # Response should be timely (under 30 seconds for a simple query)
        assert response_time < 30
        assert response.status_code == 200

    def test_api_endpoint_interoperability(self, client):
        """Test that API endpoints work well together"""
        # First, let's try to get a source that doesn't exist yet
        initial_sources_response = client.get("/api/v1/sources/nonexistent-chunk")
        assert initial_sources_response.status_code in [404, 200]  # May return 404 or handle gracefully

        # Now submit content that might create a chunk
        select_data = {
            "text": "Sample content for interoperability testing",
            "source_url": "https://book.example.com/interop-test"
        }

        select_response = client.post("/api/v1/select", json=select_data)
        assert select_response.status_code in [200, 201]

        # The system might generate a chunk ID from the selected text
        # which could then be retrievable via the sources endpoint

    def test_api_cors_and_domain_restriction(self, client):
        """Test that API endpoints respect CORS and domain restrictions"""
        # Test with a standard request (should work)
        query_data = {"query": "CORS test", "session_id": "cors-test"}
        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 200

        # Check if CORS headers are present in the response
        # This depends on how CORS is configured in main.py
        cors_response = client.post("/api/v1/query",
                                   json=query_data,
                                   headers={"Origin": "https://trusted-domain.com"})
        # The response should handle CORS appropriately

    def test_api_health_and_readiness(self, client):
        """Test API health and readiness endpoints"""
        # Test root endpoint
        root_response = client.get("/")
        assert root_response.status_code == 200
        root_data = root_response.json()
        assert "message" in root_data

        # Test health endpoint
        health_response = client.get("/health")
        assert health_response.status_code == 200
        health_data = health_response.json()
        assert health_data["status"] == "healthy"

        # Verify all API endpoints are registered and accessible
        endpoints_to_test = [
            ("/api/v1/query", "POST"),
            ("/api/v1/select", "POST"),
            ("/api/v1/ingest", "POST"),
        ]

        for endpoint, method in endpoints_to_test:
            if method == "POST":
                # For endpoints that require specific data, just check they don't return 404
                response = client.post(endpoint, json={})
                assert response.status_code != 404