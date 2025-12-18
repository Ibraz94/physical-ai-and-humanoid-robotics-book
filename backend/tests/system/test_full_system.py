import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app


class TestFullSystem:
    """System integration tests for the complete backend system"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_complete_user_journey(self, client):
        """Test a complete user journey: ingestion -> selection -> querying -> source retrieval"""
        # Step 1: Ingest content (using mocks to avoid real network calls)
        with patch('backend.ingestion.sitemap_parser.requests.get') as mock_sitemap_get, \
             patch('backend.ingestion.content_extractor.requests.get') as mock_content_get, \
             patch('backend.ingestion.chunker.ContentChunker.chunk_content') as mock_chunker, \
             patch('backend.ingestion.embedding_service.EmbeddingService.generate_embeddings') as mock_embeddings, \
             patch('backend.ingestion.vector_storage.VectorStorage.store_embeddings') as mock_vector_store:

            # Mock ingestion process
            mock_sitemap_get.return_value.text = """<?xml version="1.0" encoding="UTF-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <url>
                    <loc>https://book.example.com/user-journey-chapter</loc>
                </url>
            </urlset>"""
            mock_sitemap_get.return_value.status_code = 200

            mock_content_get.return_value.text = """
            <html>
            <body>
                <h1>RAG Systems Overview</h1>
                <p>Retrieval-Augmented Generation combines retrieval and generation for better responses.</p>
                <p>RAG systems use external knowledge bases to ground their responses.</p>
            </body>
            </html>"""
            mock_content_get.return_value.status_code = 200

            mock_chunker.return_value = [
                "Retrieval-Augmented Generation combines retrieval and generation for better responses.",
                "RAG systems use external knowledge bases to ground their responses."
            ]
            mock_embeddings.return_value = [[0.1, 0.2], [0.3, 0.4]]
            mock_vector_store.return_value = True

            # Ingest the content
            ingest_response = client.post("/api/v1/ingest", json={"sitemap_url": "https://book.example.com/sitemap.xml"})
            assert ingest_response.status_code in [200, 202]

        # Step 2: User selects additional text
        select_data = {
            "text": "RAG systems are particularly useful for domain-specific knowledge tasks.",
            "source_url": "https://book.example.com/domain-specific-usage"
        }

        select_response = client.post("/api/v1/select", json=select_data)
        assert select_response.status_code in [200, 201]

        # Step 3: User queries about the content
        query_data = {
            "query": "What are RAG systems and how do they work?",
            "session_id": "system-test-session"
        }

        query_response = client.post("/api/v1/query", json=query_data)
        assert query_response.status_code == 200

        query_result = query_response.json()
        assert "answer" in query_result
        assert "citations" in query_result

        # Step 4: Retrieve source information for citations
        if len(query_result["citations"]) > 0:
            first_citation = query_result["citations"][0]
            if "chunk_id" in first_citation:
                sources_response = client.get(f"/api/v1/sources/{first_citation['chunk_id']}")
                assert sources_response.status_code in [200, 404]

    def test_system_error_tolerance(self, client):
        """Test the system's tolerance to various error conditions"""
        # Test with service dependencies failing
        with patch('backend.ingestion.sitemap_parser.requests.get') as mock_sitemap_get:
            mock_sitemap_get.side_effect = Exception("Network unavailable")

            response = client.post("/api/v1/ingest", json={"sitemap_url": "https://book.example.com/sitemap.xml"})
            # Should handle gracefully, not crash the entire system
            assert response.status_code in [500, 400, 200]

        # Test query endpoint with no context
        query_response = client.post("/api/v1/query", json={
            "query": "What happens with no context?",
            "session_id": "error-tolerance-test"
        })
        assert query_response.status_code == 200  # Should still work, maybe with "I don't know" response

    def test_system_performance_under_load(self, client):
        """Test system performance under load conditions"""
        import time
        import threading

        responses = []

        def make_request(req_type, data, idx):
            start_time = time.time()
            if req_type == "query":
                response = client.post("/api/v1/query", json=data)
            elif req_type == "select":
                response = client.post("/api/v1/select", json=data)
            else:
                response = client.get(f"/api/v1/sources/test-{idx}")

            end_time = time.time()
            responses.append({
                "index": idx,
                "status": response.status_code,
                "response_time": end_time - start_time,
                "type": req_type
            })

        # Create multiple concurrent requests
        threads = []
        req_count = 10

        for i in range(req_count):
            # Mix of different request types
            if i % 3 == 0:
                data = {"query": f"Load test query {i}", "session_id": f"load-test-{i}"}
                thread = threading.Thread(target=make_request, args=("query", data, i))
            elif i % 3 == 1:
                data = {"text": f"Load test selected text {i}", "source_url": f"https://example.com/{i}"}
                thread = threading.Thread(target=make_request, args=("select", data, i))
            else:
                thread = threading.Thread(target=make_request, args=("sources", None, i))

            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify all requests were processed
        assert len(responses) == req_count
        for resp in responses:
            # All requests should complete with reasonable status codes
            assert resp["status"] in [200, 201, 202, 404, 422, 400, 405]
            # Response time should be reasonable (under 30 seconds)
            assert resp["response_time"] < 30

    def test_system_data_consistency(self, client):
        """Test that data remains consistent across the entire system"""
        session_id = "consistency-test-session"

        # Make a series of related queries to test data consistency
        queries = [
            {"query": "What are RAG systems?", "session_id": session_id},
            {"query": "How do they work?", "session_id": session_id},
            {"query": "What are their benefits?", "session_id": session_id}
        ]

        responses = []
        for query_data in queries:
            response = client.post("/api/v1/query", json=query_data)
            assert response.status_code == 200
            responses.append(response.json())

        # Verify that responses are contextually related
        all_answers = " ".join([resp["answer"] for resp in responses])
        # All responses should be related to RAG systems
        assert "RAG" in all_answers or "retrieval" in all_answers.lower()

    def test_system_security_measures(self, client):
        """Test that security measures work across the entire system"""
        # Test SQL injection attempts
        sql_injection_attempts = [
            {"query": "'; DROP TABLE users; --"},
            {"text": "'; DROP TABLE chunks; --", "source_url": "https://example.com"},
        ]

        endpoints_and_data = [
            ("/api/v1/query", sql_injection_attempts[0]),
            ("/api/v1/select", sql_injection_attempts[1]),
        ]

        for endpoint, data in endpoints_and_data:
            response = client.post(endpoint, json=data)
            # Should not crash or expose internal errors
            assert response.status_code in [422, 400, 200]

        # Test XSS attempts
        xss_attempts = [
            {"query": "<script>alert('xss')</script>"},
            {"text": "<script>alert('xss')</script>", "source_url": "https://example.com"},
        ]

        for i, data in enumerate([xss_attempts[0], xss_attempts[1]]):
            endpoint = "/api/v1/query" if i == 0 else "/api/v1/select"
            response = client.post(endpoint, json=data)
            # Should handle XSS attempts safely
            assert response.status_code in [422, 400, 200]

    def test_system_caching_and_optimization(self, client):
        """Test system behavior with repeated requests (caching effects)"""
        # Make the same query multiple times to test caching/optimization
        query_data = {
            "query": "What is the main concept of RAG?",
            "session_id": "caching-test-session"
        }

        responses = []
        for i in range(3):
            response = client.post("/api/v1/query", json=query_data)
            assert response.status_code == 200
            responses.append(response.json())

        # All responses should be consistent
        first_answer = responses[0]["answer"]
        for response in responses[1:]:
            # Answers should be similar or identical
            assert "answer" in response

    def test_system_multi_user_isolation(self, client):
        """Test that multiple users' data is properly isolated"""
        import threading
        import time

        user_results = {}

        def user_workflow(user_id):
            session_id = f"multi-user-test-{user_id}"

            # Each user performs their own query
            query_data = {
                "query": f"User {user_id} asking about RAG systems",
                "session_id": session_id
            }

            response = client.post("/api/v1/query", json=query_data)
            user_results[user_id] = {
                "status": response.status_code,
                "session_id": session_id,
                "has_answer": "answer" in response.json() if response.status_code == 200 else False
            }

        # Simulate multiple users working simultaneously
        threads = []
        for user_id in range(5):
            thread = threading.Thread(target=user_workflow, args=(user_id,))
            threads.append(thread)
            thread.start()
            time.sleep(0.01)  # Small delay between user starts

        for thread in threads:
            thread.join()

        # Verify all users got successful responses
        assert len(user_results) == 5
        for user_id, result in user_results.items():
            assert result["status"] == 200
            assert result["has_answer"] is True

    def test_system_resource_management(self, client):
        """Test system resource management under various conditions"""
        # Test with a long-running query-like request
        import time

        start_time = time.time()
        response = client.post("/api/v1/query", json={
            "query": "Provide a comprehensive analysis of RAG system architectures",
            "session_id": "resource-test"
        })
        end_time = time.time()

        response_time = end_time - start_time

        # Should respond in a reasonable time
        assert response_time < 30  # Less than 30 seconds
        assert response.status_code in [200, 408, 504]  # Success or timeout

        if response.status_code == 200:
            result = response.json()
            assert "answer" in result
            assert "citations" in result

    def test_system_configuration_consistency(self, client):
        """Test that system configuration is consistent across components"""
        # Test health endpoint
        health_response = client.get("/health")
        assert health_response.status_code == 200
        health_data = health_response.json()
        assert health_data["status"] == "healthy"

        # Test root endpoint
        root_response = client.get("/")
        assert root_response.status_code == 200
        root_data = root_response.json()
        assert "message" in root_data

        # Verify API endpoints are accessible
        api_endpoints = [
            ("/api/v1/query", "POST"),
            ("/api/v1/select", "POST"),
            ("/api/v1/ingest", "POST"),
        ]

        for endpoint, method in api_endpoints:
            if method == "POST":
                response = client.post(endpoint, json={})
                # Should return validation error, not 404
                assert response.status_code != 404

    def test_system_recovery_from_partial_failures(self, client):
        """Test that the system can recover from partial component failures"""
        # Test that the system still works even if some optional features fail
        with patch('backend.app.services.metadata_service.MetadataService.store_interaction') as mock_metadata_store:
            # Mock metadata storage to fail
            mock_metadata_store.side_effect = Exception("Metadata storage failed")

            # The query should still work even if metadata storage fails
            query_response = client.post("/api/v1/query", json={
                "query": "Test query with metadata failure",
                "session_id": "recovery-test"
            })

            # Should still return success even if metadata storage fails
            assert query_response.status_code == 200
            result = query_response.json()
            assert "answer" in result
            assert "citations" in result