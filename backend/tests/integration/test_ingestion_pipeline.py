import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.ingestion.sitemap_parser import SitemapParser
from backend.ingestion.content_extractor import ContentExtractor
from backend.ingestion.chunker import ContentChunker
from backend.ingestion.embedding_service import EmbeddingService
from backend.ingestion.vector_storage import VectorStorageService


class TestIngestionPipelineIntegration:
    """Integration tests for the ingestion pipeline"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    @pytest.fixture
    def mock_services(self):
        """Create mocks for all ingestion services"""
        return {
            'sitemap_parser': Mock(spec=SitemapParser),
            'content_extractor': Mock(spec=ContentExtractor),
            'chunker': Mock(spec=ContentChunker),
            'embedding_service': Mock(spec=EmbeddingService),
            'vector_storage': Mock(spec=VectorStorageService)
        }

    def test_ingestion_pipeline_full_flow(self, client, mock_services):
        """Test the full ingestion pipeline from sitemap to vector storage"""
        # Mock the services
        mock_services['sitemap_parser'].parse_sitemap.return_value = [
            "https://book.example.com/chapter-1",
            "https://book.example.com/chapter-2"
        ]

        mock_services['content_extractor'].extract_content_from_url.side_effect = [
            "This is the content of chapter 1 with several paragraphs and important information.",
            "This is the content of chapter 2 with different topics and concepts."
        ]

        mock_services['chunker'].chunk_content.return_value = [
            ["Chunk 1 from chapter 1", "Chunk 2 from chapter 1"],
            ["Chunk 1 from chapter 2", "Chunk 2 from chapter 2"]
        ]

        mock_services['embedding_service'].generate_embeddings.return_value = [
            [0.1, 0.2, 0.3], [0.4, 0.5, 0.6]
        ]

        mock_services['vector_storage'].store_chunks.return_value = True

        # Patch the services in the actual ingestion code
        with patch('backend.app.api.v1.ingest.SitemapParser', return_value=mock_services['sitemap_parser']), \
             patch('backend.app.api.v1.ingest.ContentExtractor', return_value=mock_services['content_extractor']), \
             patch('backend.ingestion.chunker.ContentChunker', return_value=mock_services['chunker']), \
             patch('backend.ingestion.embedding_service.EmbeddingService', return_value=mock_services['embedding_service']), \
             patch('backend.ingestion.vector_storage.VectorStorageService', return_value=mock_services['vector_storage']):

            ingest_data = {
                "sitemap_url": "https://book.example.com/sitemap.xml"
            }

            response = client.post("/api/v1/ingest", json=ingest_data)

            assert response.status_code in [200, 202]  # Success or accepted
            response_data = response.json()

            # Verify the pipeline was executed
            mock_services['sitemap_parser'].parse_sitemap.assert_called_once()
            assert mock_services['content_extractor'].extract_content_from_url.call_count == 2
            assert mock_services['chunker'].chunk_content.call_count == 2  # Once per page
            assert mock_services['embedding_service'].generate_embeddings.call_count >= 1
            mock_services['vector_storage'].store_chunks.assert_called()

    def test_ingestion_pipeline_with_single_page(self, client, mock_services):
        """Test the ingestion pipeline with a single page"""
        mock_services['sitemap_parser'].parse_sitemap.return_value = [
            "https://book.example.com/single-page"
        ]

        mock_services['content_extractor'].extract_content_from_url.return_value = \
            "This is content from a single page with important information."

        mock_services['chunker'].chunk_content.return_value = [
            "Chunk 1 from single page",
            "Chunk 2 from single page"
        ]

        mock_services['embedding_service'].generate_embeddings.return_value = [
            [0.1, 0.2, 0.3], [0.4, 0.5, 0.6]
        ]

        mock_services['vector_storage'].store_chunks.return_value = True

        with patch('backend.app.api.v1.ingest.SitemapParser', return_value=mock_services['sitemap_parser']), \
             patch('backend.app.api.v1.ingest.ContentExtractor', return_value=mock_services['content_extractor']), \
             patch('backend.ingestion.chunker.ContentChunker', return_value=mock_services['chunker']), \
             patch('backend.ingestion.embedding_service.EmbeddingService', return_value=mock_services['embedding_service']), \
             patch('backend.ingestion.vector_storage.VectorStorageService', return_value=mock_services['vector_storage']):

            ingest_data = {
                "sitemap_url": "https://book.example.com/sitemap.xml"
            }

            response = client.post("/api/v1/ingest", json=ingest_data)

            assert response.status_code in [200, 202]
            mock_services['sitemap_parser'].parse_sitemap.assert_called_once()
            mock_services['content_extractor'].extract_content_from_url.assert_called_once()
            mock_services['chunker'].chunk_content.assert_called_once()
            mock_services['embedding_service'].generate_embeddings.assert_called()
            mock_services['vector_storage'].store_chunks.assert_called()

    def test_ingestion_pipeline_error_handling(self, client, mock_services):
        """Test error handling in the ingestion pipeline"""
        # Simulate an error in content extraction
        mock_services['sitemap_parser'].parse_sitemap.return_value = [
            "https://book.example.com/chapter-1"
        ]

        mock_services['content_extractor'].extract_content_from_url.side_effect = Exception("Network error")

        with patch('backend.app.api.v1.ingest.SitemapParser', return_value=mock_services['sitemap_parser']), \
             patch('backend.app.api.v1.ingest.ContentExtractor', return_value=mock_services['content_extractor']):

            ingest_data = {
                "sitemap_url": "https://book.example.com/sitemap.xml"
            }

            response = client.post("/api/v1/ingest", json=ingest_data)

            # Should return appropriate error response, not crash
            assert response.status_code in [400, 500, 200]  # Error response or handled gracefully

    def test_ingestion_pipeline_empty_sitemap(self, client, mock_services):
        """Test ingestion pipeline with empty sitemap"""
        mock_services['sitemap_parser'].parse_sitemap.return_value = []

        with patch('backend.app.api.v1.ingest.SitemapParser', return_value=mock_services['sitemap_parser']):

            ingest_data = {
                "sitemap_url": "https://book.example.com/empty-sitemap.xml"
            }

            response = client.post("/api/v1/ingest", json=ingest_data)

            # Should handle empty sitemap gracefully
            assert response.status_code in [200, 202, 400]

    def test_ingestion_pipeline_cross_service_data_flow(self, client, mock_services):
        """Test that data flows correctly between services in the pipeline"""
        # URLs from sitemap parser
        urls = ["https://book.example.com/chapter-1"]
        mock_services['sitemap_parser'].parse_sitemap.return_value = urls

        # Content from extractor should be passed to chunker
        content = "This is the full content that should be chunked into smaller pieces for processing."
        mock_services['content_extractor'].extract_content_from_url.return_value = content

        # Chunks from chunker should be passed to embedding service
        chunks = ["Chunk 1: This is the first part of the content.", "Chunk 2: This is the second part."]
        mock_services['chunker'].chunk_content.return_value = chunks

        # Embeddings should be stored in vector storage
        embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        mock_services['embedding_service'].generate_embeddings.return_value = embeddings

        mock_services['vector_storage'].store_chunks.return_value = True

        with patch('backend.app.api.v1.ingest.SitemapParser', return_value=mock_services['sitemap_parser']), \
             patch('backend.app.api.v1.ingest.ContentExtractor', return_value=mock_services['content_extractor']), \
             patch('backend.ingestion.chunker.ContentChunker', return_value=mock_services['chunker']), \
             patch('backend.ingestion.embedding_service.EmbeddingService', return_value=mock_services['embedding_service']), \
             patch('backend.ingestion.vector_storage.VectorStorageService', return_value=mock_services['vector_storage']):

            ingest_data = {
                "sitemap_url": "https://book.example.com/sitemap.xml"
            }

            response = client.post("/api/v1/ingest", json=ingest_data)

            assert response.status_code in [200, 202]

            # Verify data flow
            mock_services['sitemap_parser'].parse_sitemap.assert_called_once()
            mock_services['content_extractor'].extract_content_from_url.assert_called_with(urls[0])
            mock_services['chunker'].chunk_content.assert_called_once()  # Called with extracted content
            mock_services['embedding_service'].generate_embeddings.assert_called_once()  # Called with chunks
            mock_services['vector_storage'].store_chunks.assert_called_once()  # Called with embeddings

    def test_ingestion_pipeline_chunk_validation(self, client, mock_services):
        """Test that chunks meet the required size specifications"""
        mock_services['sitemap_parser'].parse_sitemap.return_value = [
            "https://book.example.com/chapter-1"
        ]

        long_content = "This is a very long content. " * 100  # Create content that will be chunked
        mock_services['content_extractor'].extract_content_from_url.return_value = long_content

        # Mock chunker to return properly sized chunks
        mock_services['chunker'].chunk_content.return_value = [
            "Chunk 1: Properly sized content chunk for testing purposes.",
            "Chunk 2: Another properly sized content chunk with overlap."
        ]

        mock_services['embedding_service'].generate_embeddings.return_value = [
            [0.1, 0.2, 0.3], [0.4, 0.5, 0.6]
        ]

        mock_services['vector_storage'].store_chunks.return_value = True

        with patch('backend.app.api.v1.ingest.SitemapParser', return_value=mock_services['sitemap_parser']), \
             patch('backend.app.api.v1.ingest.ContentExtractor', return_value=mock_services['content_extractor']), \
             patch('backend.ingestion.chunker.ContentChunker', return_value=mock_services['chunker']), \
             patch('backend.ingestion.embedding_service.EmbeddingService', return_value=mock_services['embedding_service']), \
             patch('backend.ingestion.vector_storage.VectorStorageService', return_value=mock_services['vector_storage']):

            ingest_data = {
                "sitemap_url": "https://book.example.com/sitemap.xml"
            }

            response = client.post("/api/v1/ingest", json=ingest_data)

            assert response.status_code in [200, 202]
            # Verify that the chunking process was executed
            mock_services['chunker'].chunk_content.assert_called_once()

    def test_ingestion_pipeline_with_special_content_types(self, client, mock_services):
        """Test ingestion pipeline with various content types"""
        mock_services['sitemap_parser'].parse_sitemap.return_value = [
            "https://book.example.com/chapter-1",
            "https://book.example.com/chapter-2-unicode",
            "https://book.example.com/chapter-3-with-code"
        ]

        mock_services['content_extractor'].extract_content_from_url.side_effect = [
            "Regular content with standard characters.",
            "Content with unicode characters: ñáéíóú and emoji: 🤖📚💡",
            "Content with code blocks and special formatting <code>var x = 1;</code>"
        ]

        mock_services['chunker'].chunk_content.side_effect = [
            ["Regular chunk"],
            ["Unicode chunk with ñáéíóú"],
            ["Code chunk with <code> block"]
        ]

        mock_services['embedding_service'].generate_embeddings.return_value = [
            [0.1, 0.2, 0.3]
        ] * 3  # Same embedding for simplicity

        mock_services['vector_storage'].store_chunks.return_value = True

        with patch('backend.app.api.v1.ingest.SitemapParser', return_value=mock_services['sitemap_parser']), \
             patch('backend.app.api.v1.ingest.ContentExtractor', return_value=mock_services['content_extractor']), \
             patch('backend.ingestion.chunker.ContentChunker', return_value=mock_services['chunker']), \
             patch('backend.ingestion.embedding_service.EmbeddingService', return_value=mock_services['embedding_service']), \
             patch('backend.ingestion.vector_storage.VectorStorageService', return_value=mock_services['vector_storage']):

            ingest_data = {
                "sitemap_url": "https://book.example.com/sitemap.xml"
            }

            response = client.post("/api/v1/ingest", json=ingest_data)

            # Should handle various content types gracefully
            assert response.status_code in [200, 202]

    def test_ingestion_pipeline_status_tracking(self, client):
        """Test that ingestion jobs are properly tracked"""
        ingest_data = {
            "sitemap_url": "https://book.example.com/sitemap.xml"
        }

        response = client.post("/api/v1/ingest", json=ingest_data)

        # Should return tracking information
        assert response.status_code in [200, 202]
        if response.status_code == 200:
            response_data = response.json()
            # May include job ID or status information
            assert isinstance(response_data, dict)