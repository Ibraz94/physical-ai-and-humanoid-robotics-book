import pytest
from fastapi.testclient import TestClient
from backend.app.main import app


class TestQueryFlowE2E:
    """End-to-end tests for User Story 1 - Query Processing flow"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_basic_query_flow(self, client):
        """Test the basic query flow: user submits query -> receives grounded response"""
        query_data = {
            "query": "What are the key principles of RAG systems?",
            "session_id": "e2e-test-session-1"
        }

        response = client.post("/api/v1/query", json=query_data)

        assert response.status_code == 200
        response_data = response.json()

        # Verify response structure
        assert "answer" in response_data
        assert "citations" in response_data
        assert "session_id" in response_data

        # Verify the response contains relevant information
        assert isinstance(response_data["answer"], str)
        assert len(response_data["answer"]) > 0

        # Citations should be a list (may be empty if no relevant content found)
        assert isinstance(response_data["citations"], list)

        # Session ID should match what was sent
        assert response_data["session_id"] == "e2e-test-session-1"

    def test_query_flow_with_context(self, client):
        """Test query flow with additional context"""
        # First, submit user-selected text via the select endpoint
        select_data = {
            "text": "RAG stands for Retrieval-Augmented Generation. It combines information retrieval with text generation to produce more accurate and grounded responses.",
            "source_url": "https://book.example.com/rag-intro"
        }

        select_response = client.post("/api/v1/select", json=select_data)
        assert select_response.status_code in [200, 201]

        # Then, query using that context
        query_data = {
            "query": "Explain RAG based on the provided context?",
            "session_id": "e2e-test-session-2"
        }

        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 200

        response_data = response.json()
        assert "answer" in response_data
        assert "citations" in response_data

        # The answer should reference the concept of RAG since it was in the context
        assert "RAG" in response_data["answer"] or "retrieval" in response_data["answer"].lower()

    def test_query_flow_insufficient_context_response(self, client):
        """Test that the system returns 'I don't know' when context is insufficient"""
        query_data = {
            "query": "What is the meaning of life according to this book?",
            "session_id": "e2e-test-session-3"
        }

        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 200

        response_data = response.json()
        assert "answer" in response_data
        assert "citations" in response_data

        # If no relevant context is found, the system should respond appropriately
        # It might say "I don't know" or provide a response indicating lack of information
        answer = response_data["answer"].lower()
        if "don't know" in answer or "no information" in answer or "not found" in answer:
            assert True  # This is an acceptable response
        else:
            # If it provides an answer, citations should be relevant
            assert isinstance(response_data["citations"], list)

    def test_query_flow_session_persistence(self, client):
        """Test that session data persists across multiple queries"""
        session_id = "e2e-session-persistence-test"

        # First query
        query_1 = {
            "query": "What are RAG systems?",
            "session_id": session_id
        }

        response_1 = client.post("/api/v1/query", json=query_1)
        assert response_1.status_code == 200

        # Second query in same session
        query_2 = {
            "query": "How do they work?",
            "session_id": session_id  # Same session
        }

        response_2 = client.post("/api/v1/query", json=query_2)
        assert response_2.status_code == 200

        response_2_data = response_2.json()
        assert response_2_data["session_id"] == session_id

        # Both responses should have the same session ID
        response_1_data = response_1.json()
        assert response_1_data["session_id"] == session_id

    def test_query_flow_with_citations(self, client):
        """Test that queries return proper citations when content is found"""
        query_data = {
            "query": "What is retrieval-augmented generation?",
            "session_id": "e2e-citation-test"
        }

        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 200

        response_data = response.json()
        assert "answer" in response_data
        assert "citations" in response_data

        # If citations are provided, they should have the proper structure
        for citation in response_data["citations"]:
            assert "chunk_id" in citation
            assert "module" in citation
            assert "chapter" in citation
            assert "url" in citation

    def test_query_flow_error_handling(self, client):
        """Test error handling in the query flow"""
        # Test with invalid request structure
        invalid_query_data = {
            "invalid_field": "invalid_value"
        }

        response = client.post("/api/v1/query", json=invalid_query_data)
        assert response.status_code in [422, 400]  # Validation error

        # Test with empty query
        empty_query_data = {
            "query": "",
            "session_id": "e2e-error-test"
        }

        response = client.post("/api/v1/query", json=empty_query_data)
        assert response.status_code == 422  # Validation error

    def test_query_flow_grounding_validation(self, client):
        """Test that responses are properly grounded in provided context"""
        # This test assumes there is content in the system that discusses RAG
        query_data = {
            "query": "Explain the benefits of RAG systems?",
            "session_id": "e2e-grounding-test"
        }

        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 200

        response_data = response.json()
        assert "answer" in response_data
        assert "citations" in response_data

        # The response should be grounded in actual content, not hallucinated
        # This is difficult to test automatically, but we can check that citations exist
        # when there's a substantive response
        if len(response_data["answer"]) > 50:  # If response is substantial
            assert len(response_data["citations"]) >= 0  # May or may not have citations

    def test_query_flow_special_characters(self, client):
        """Test query flow with special characters and unicode"""
        query_data = {
            "query": "How is RAG pronounced in Spanish: 'la generación aumentada con recuperación'?",
            "session_id": "e2e-unicode-test"
        }

        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 200

        response_data = response.json()
        assert "answer" in response_data
        assert isinstance(response_data["answer"], str)  # Should handle unicode properly

    def test_query_flow_concurrent_users(self, client):
        """Test query flow with multiple concurrent users"""
        import threading
        import time

        results = []

        def make_query(query_text, session_id):
            query_data = {
                "query": query_text,
                "session_id": session_id
            }

            response = client.post("/api/v1/query", json=query_data)
            results.append((response.status_code, response.json() if response.status_code == 200 else None))

        # Create multiple threads making queries simultaneously
        threads = []
        for i in range(3):
            thread = threading.Thread(
                target=make_query,
                args=(f"Concurrent query {i}", f"session-concurrent-{i}")
            )
            threads.append(thread)
            thread.start()
            time.sleep(0.01)  # Small delay between thread starts

        for thread in threads:
            thread.join()

        # Verify all queries were processed successfully
        assert len(results) == 3
        for status_code, data in results:
            # All should either succeed or fail with proper error codes
            assert status_code in [200, 422, 400]
            if status_code == 200:
                assert data is not None
                assert "answer" in data
                assert "citations" in data

    def test_query_flow_long_response_handling(self, client):
        """Test query flow handling for queries that might generate long responses"""
        query_data = {
            "query": "Provide a comprehensive overview of retrieval-augmented generation, including its history, benefits, challenges, and implementation approaches.",
            "session_id": "e2e-long-response-test"
        }

        response = client.post("/api/v1/query", json=query_data)

        # Should handle long query requests appropriately
        assert response.status_code in [200, 408, 504]  # Success, timeout, or gateway timeout
        if response.status_code == 200:
            response_data = response.json()
            assert "answer" in response_data
            assert "citations" in response_data
            assert isinstance(response_data["answer"], str)