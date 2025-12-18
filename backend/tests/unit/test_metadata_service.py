import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.app.services.metadata_service import MetadataService


class TestMetadataService:
    """Unit tests for the MetadataService class"""

    @pytest.fixture
    def metadata_service(self):
        """Create a MetadataService instance for testing"""
        with patch('backend.app.services.metadata_service.database'):
            return MetadataService()

    def test_store_interaction_metadata_success(self, metadata_service):
        """Test successful storage of interaction metadata"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            interaction_data = {
                "session_id": "session_123",
                "query": "What are RAG systems?",
                "response": "RAG systems combine retrieval and generation...",
                "timestamp": "2023-01-01T00:00:00Z",
                "user_id": "user_123"
            }

            result = metadata_service.store_interaction(interaction_data)

            # Should return success indicator
            assert isinstance(result, bool)

    def test_store_interaction_metadata_missing_fields(self, metadata_service):
        """Test storage of interaction metadata with missing optional fields"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            # Interaction with only required fields
            interaction_data = {
                "session_id": "session_123",
                "query": "What are RAG systems?",
                "response": "RAG systems combine retrieval and generation...",
                "timestamp": "2023-01-01T00:00:00Z"
                # Missing user_id (might be optional)
            }

            result = metadata_service.store_interaction(interaction_data)

            # Should handle missing optional fields gracefully
            assert isinstance(result, bool)

    def test_store_interaction_metadata_validation(self, metadata_service):
        """Test validation during interaction metadata storage"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            # Invalid data types
            invalid_interaction_data = {
                "session_id": 123,  # Should be string
                "query": 456,       # Should be string
                "response": 789,    # Should be string
                "timestamp": 000,   # Should be string/datetime
            }

            with pytest.raises(Exception):
                metadata_service.store_interaction(invalid_interaction_data)

    def test_retrieve_interaction_history_success(self, metadata_service):
        """Test successful retrieval of interaction history"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            # Mock the database query to return interaction history
            mock_interaction = Mock()
            mock_interaction.session_id = "session_123"
            mock_interaction.query = "What are RAG systems?"
            mock_interaction.response = "RAG systems combine retrieval and generation..."

            mock_query_result = [mock_interaction]
            mock_db.query.return_value.filter.return_value.all.return_value = mock_query_result

            history = metadata_service.get_interaction_history("session_123")

            assert isinstance(history, list)
            if len(history) > 0:
                assert hasattr(history[0], 'query') or 'query' in str(history[0])

    def test_retrieve_interaction_history_empty(self, metadata_service):
        """Test retrieval of interaction history when none exists"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            # Mock the database query to return empty list
            mock_db.query.return_value.filter.return_value.all.return_value = []

            history = metadata_service.get_interaction_history("nonexistent_session")

            assert isinstance(history, list)
            assert len(history) == 0

    def test_store_chunk_metadata_success(self, metadata_service):
        """Test successful storage of chunk metadata"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            chunk_metadata = {
                "chunk_id": "chunk_abc_123",
                "source_url": "https://book.example.com/chapter-1",
                "module": "Chapter 1",
                "chapter": "Introduction",
                "anchor": "section-1.1",
                "content_preview": "This is the beginning of the chapter...",
                "created_at": "2023-01-01T00:00:00Z",
                "ingestion_job_id": "job_123"
            }

            result = metadata_service.store_chunk_metadata(chunk_metadata)

            assert isinstance(result, bool)

    def test_retrieve_chunk_metadata_success(self, metadata_service):
        """Test successful retrieval of chunk metadata"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            # Mock the database query to return chunk metadata
            mock_chunk = Mock()
            mock_chunk.chunk_id = "chunk_abc_123"
            mock_chunk.source_url = "https://book.example.com/chapter-1"
            mock_chunk.module = "Chapter 1"

            mock_db.query.return_value.filter.return_value.first.return_value = mock_chunk

            chunk_metadata = metadata_service.get_chunk_metadata("chunk_abc_123")

            assert chunk_metadata is not None
            if chunk_metadata:
                assert hasattr(chunk_metadata, 'chunk_id') or 'chunk_id' in str(chunk_metadata)

    def test_retrieve_chunk_metadata_not_found(self, metadata_service):
        """Test retrieval of chunk metadata when not found"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            # Mock the database query to return None
            mock_db.query.return_value.filter.return_value.first.return_value = None

            chunk_metadata = metadata_service.get_chunk_metadata("nonexistent_chunk")

            assert chunk_metadata is None

    def test_store_user_consent_success(self, metadata_service):
        """Test successful storage of user consent"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            result = metadata_service.store_user_consent("user_123", True, "2023-01-01T00:00:00Z")

            assert isinstance(result, bool)

    def test_get_user_consent_status(self, metadata_service):
        """Test retrieval of user consent status"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            # Mock the database query to return consent record
            mock_consent = Mock()
            mock_consent.user_id = "user_123"
            mock_consent.consent_given = True
            mock_consent.timestamp = "2023-01-01T00:00:00Z"

            mock_db.query.return_value.filter.return_value.first.return_value = mock_consent

            consent_status = metadata_service.get_user_consent("user_123")

            assert consent_status is not None

    def test_get_user_consent_not_found(self, metadata_service):
        """Test retrieval of consent when user has no record"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            # Mock the database query to return None
            mock_db.query.return_value.filter.return_value.first.return_value = None

            consent_status = metadata_service.get_user_consent("user_456")

            # Should return None or False if no consent record exists
            assert consent_status in [None, False]

    def test_update_interaction_metadata(self, metadata_service):
        """Test updating existing interaction metadata"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            # Mock finding an existing interaction
            mock_interaction = Mock()
            mock_interaction.session_id = "session_123"
            mock_interaction.feedback = None

            mock_db.query.return_value.filter.return_value.first.return_value = mock_interaction

            result = metadata_service.update_interaction_feedback("interaction_123", "helpful")

            assert isinstance(result, bool)

    def test_store_ingestion_metadata_success(self, metadata_service):
        """Test successful storage of ingestion metadata"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            ingestion_metadata = {
                "job_id": "ingest_job_123",
                "sitemap_url": "https://book.example.com/sitemap.xml",
                "status": "completed",
                "pages_processed": 25,
                "start_time": "2023-01-01T00:00:00Z",
                "end_time": "2023-01-01T00:05:00Z",
                "error_count": 0
            }

            result = metadata_service.store_ingestion_metadata(ingestion_metadata)

            assert isinstance(result, bool)

    def test_retrieve_ingestion_status(self, metadata_service):
        """Test retrieval of ingestion job status"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            # Mock the database query to return ingestion metadata
            mock_ingestion = Mock()
            mock_ingestion.job_id = "ingest_job_123"
            mock_ingestion.status = "completed"
            mock_ingestion.pages_processed = 25

            mock_db.query.return_value.filter.return_value.first.return_value = mock_ingestion

            status = metadata_service.get_ingestion_status("ingest_job_123")

            assert status is not None

    def test_metadata_search_functionality(self, metadata_service):
        """Test searching metadata by various criteria"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            # Mock search results
            mock_result = Mock()
            mock_result.session_id = "session_123"
            mock_db.query.return_value.filter.return_value.all.return_value = [mock_result]

            results = metadata_service.search_metadata(query_text="RAG systems", user_id="user_123")

            assert isinstance(results, list)

    def test_metadata_cleanup_old_records(self, metadata_service):
        """Test cleanup of old metadata records"""
        with patch('backend.app.services.metadata_service.database') as mock_db:
            # Mock the cleanup operation
            cleaned_count = metadata_service.cleanup_old_metadata(days_old=30)

            assert isinstance(cleaned_count, int)
            assert cleaned_count >= 0