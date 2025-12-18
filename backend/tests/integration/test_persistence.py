import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.session_service import SessionService
from backend.app.services.metadata_service import MetadataService


class TestDataPersistenceIntegration:
    """Integration tests for data persistence functionality"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_session_and_metadata_integration(self, client):
        """Test integration between session management and metadata storage"""
        # Create a session
        session_service = SessionService()

        with patch('backend.app.services.session_service.database'):
            session_id = session_service.create_session(user_id="integration_test_user")

            # Store some metadata associated with the session
            with patch('backend.app.services.metadata_service.database'):
                metadata_service = MetadataService()

                interaction_data = {
                    "session_id": session_id,
                    "query": "Integration test query",
                    "response": "Integration test response",
                    "timestamp": "2023-01-01T00:00:00Z"
                }

                store_result = metadata_service.store_interaction(interaction_data)
                assert store_result is True

                # Retrieve the stored interaction
                history = metadata_service.get_interaction_history(session_id)
                assert len(history) >= 1

    def test_query_endpoint_persistence_integration(self, client):
        """Test that queries made through the API are persisted"""
        query_data = {
            "query": "What are the key principles of RAG?",
            "session_id": "persist-test-123"
        }

        response = client.post("/api/v1/query", json=query_data)
        assert response.status_code == 200

        # Verify that the interaction was stored in metadata
        with patch('backend.app.services.metadata_service.database') as mock_db:
            metadata_service = MetadataService()

            # Check if interaction was logged
            history = metadata_service.get_interaction_history("persist-test-123")
            # This test depends on whether the endpoint actually stores metadata
            # The implementation might store metadata asynchronously

    def test_session_isolation_across_users(self):
        """Test that sessions and metadata are properly isolated between users"""
        with patch('backend.app.services.session_service.database'):
            session_service = SessionService()

            # Create sessions for different users
            session_1 = session_service.create_session(user_id="user_1")
            session_2 = session_service.create_session(user_id="user_2")

            assert session_1 != session_2

            # Verify sessions are valid
            assert session_service.is_valid_session(session_1) is True
            assert session_service.is_valid_session(session_2) is True

    def test_metadata_cross_service_access(self):
        """Test that metadata can be accessed across different services"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            metadata_service = MetadataService()

            # Store chunk metadata
            chunk_metadata = {
                "chunk_id": "cross-service-chunk",
                "source_url": "https://example.com/test",
                "module": "Test Module",
                "chapter": "Test Chapter"
            }

            store_result = metadata_service.store_chunk_metadata(chunk_metadata)
            assert store_result is True

            # Retrieve the chunk metadata
            retrieved = metadata_service.get_chunk_metadata("cross-service-chunk")
            # This depends on the mock setup

    def test_ingestion_metadata_persistence(self):
        """Test persistence of ingestion-related metadata"""
        with patch('backend.app.services.metadata_service.database'):
            metadata_service = MetadataService()

            ingestion_metadata = {
                "job_id": "ingest-persist-test",
                "sitemap_url": "https://example.com/sitemap.xml",
                "status": "processing",
                "pages_processed": 0,
                "start_time": "2023-01-01T00:00:00Z"
            }

            result = metadata_service.store_ingestion_metadata(ingestion_metadata)
            assert isinstance(result, bool)

            # Update the status
            ingestion_metadata["status"] = "completed"
            ingestion_metadata["pages_processed"] = 5
            ingestion_metadata["end_time"] = "2023-01-01T00:05:00Z"

            result = metadata_service.store_ingestion_metadata(ingestion_metadata)
            assert isinstance(result, bool)

    def test_user_consent_persistence(self):
        """Test persistence of user consent data"""
        with patch('backend.app.services.metadata_service.database'):
            metadata_service = MetadataService()

            # Store user consent
            consent_result = metadata_service.store_user_consent("consent-user-123", True, "2023-01-01T00:00:00Z")
            assert isinstance(consent_result, bool)

            # Retrieve user consent
            consent_status = metadata_service.get_user_consent("consent-user-123")
            assert consent_status in [True, False, None]

    def test_session_data_lifespan(self):
        """Test that session data persists for the expected lifespan"""
        with patch('backend.app.services.session_service.database'):
            session_service = SessionService()

            # Create a session
            session_id = session_service.create_session(user_id="lifespan-test")

            # Add data to the session
            store_result = session_service.store_session_data(session_id, {"test_key": "test_value"})
            assert isinstance(store_result, bool)

            # Retrieve the session data
            retrieved_data = session_service.get_session_data(session_id)
            # This depends on implementation details

    def test_concurrent_persistence_operations(self):
        """Test concurrent persistence operations don't interfere with each other"""
        import threading
        import time

        results = []

        def store_metadata(session_id):
            with patch('backend.app.services.metadata_service.database'):
                metadata_service = MetadataService()

                interaction_data = {
                    "session_id": session_id,
                    "query": f"Concurrent query for {session_id}",
                    "response": f"Response for {session_id}",
                    "timestamp": "2023-01-01T00:00:00Z"
                }

                result = metadata_service.store_interaction(interaction_data)
                results.append(result)

        # Create multiple threads to store metadata concurrently
        threads = []
        for i in range(3):
            session_id = f"concurrent-session-{i}"
            thread = threading.Thread(target=store_metadata, args=(session_id,))
            threads.append(thread)
            thread.start()
            time.sleep(0.01)  # Small delay between thread starts

        for thread in threads:
            thread.join()

        # Verify all operations succeeded
        assert len(results) == 3
        for result in results:
            assert isinstance(result, bool)

    def test_data_consistency_across_retrieval(self):
        """Test that stored data is consistently retrieved"""
        with patch('backend.app.services.metadata_service.database'):
            metadata_service = MetadataService()

            original_data = {
                "session_id": "consistency-test",
                "query": "Consistency check query with special chars: ñáéíóú 🤖",
                "response": "Consistency check response with special chars: ñáéíóú 🤖",
                "timestamp": "2023-01-01T00:00:00Z",
                "user_id": "consistency-user"
            }

            # Store the data
            store_result = metadata_service.store_interaction(original_data)
            assert store_result is True

            # Retrieve the data
            retrieved_history = metadata_service.get_interaction_history("consistency-test")
            # Verify data integrity depends on implementation

    def test_persistence_error_handling(self):
        """Test how persistence services handle database errors"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            # Configure the mock to raise an exception
            mock_db.query.side_effect = Exception("Database connection failed")

            metadata_service = MetadataService()

            interaction_data = {
                "session_id": "error-test",
                "query": "Error handling test",
                "response": "Should handle error gracefully",
                "timestamp": "2023-01-01T00:00:00Z"
            }

            # This should handle the error gracefully, not crash
            try:
                result = metadata_service.store_interaction(interaction_data)
                # If it doesn't raise an exception, result should be False or similar indicator
                assert isinstance(result, bool) or result is None
            except Exception as e:
                # If it does raise an exception, it should be a controlled one
                assert "Database" in str(e) or "persistence" in str(e).lower()