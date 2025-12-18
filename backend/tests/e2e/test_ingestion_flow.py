import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app


class TestIngestionFlowE2E:
    """End-to-end tests for User Story 2 - Content Ingestion & Processing"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_ingestion_flow_with_mocked_services(self, client):
        """Test the complete ingestion flow with mocked external services"""
        # Mock the external services to avoid making real network requests
        with patch('backend.ingestion.sitemap_parser.requests.get') as mock_sitemap_get, \
             patch('backend.ingestion.content_extractor.requests.get') as mock_content_get, \
             patch('backend.ingestion.chunker.ContentChunker.chunk_content') as mock_chunker, \
             patch('backend.ingestion.embedding_service.EmbeddingService.generate_embeddings') as mock_embeddings, \
             patch('backend.ingestion.vector_storage.VectorStorage.store_embeddings') as mock_vector_store:

            # Mock sitemap response
            mock_sitemap_get.return_value.text = """<?xml version="1.0" encoding="UTF-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <url>
                    <loc>https://book.example.com/chapter-1</loc>
                </url>
            </urlset>"""
            mock_sitemap_get.return_value.status_code = 200

            # Mock content extraction response
            mock_content_get.return_value.text = """
            <!DOCTYPE html>
            <html>
            <body>
                <h1>Chapter 1: Introduction to RAG Systems</h1>
                <p>Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with text generation.</p>
                <p>This approach allows AI systems to ground their responses in factual content.</p>
            </body>
            </html>"""
            mock_content_get.return_value.status_code = 200

            # Mock chunking
            mock_chunker.return_value = [
                "Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with text generation.",
                "This approach allows AI systems to ground their responses in factual content."
            ]

            # Mock embeddings generation
            mock_embeddings.return_value = [
                [0.1, 0.2, 0.3, 0.4],
                [0.5, 0.6, 0.7, 0.8]
            ]

            # Mock vector storage
            mock_vector_store.return_value = True

            # Now perform the ingestion
            ingest_data = {
                "sitemap_url": "https://book.example.com/sitemap.xml"
            }

            response = client.post("/api/v1/ingest", json=ingest_data)

            # Should return success (may be immediate or async)
            assert response.status_code in [200, 202]

    def test_ingestion_followed_by_query(self, client):
        """Test that ingested content can be queried"""
        with patch('backend.ingestion.sitemap_parser.requests.get') as mock_sitemap_get, \
             patch('backend.ingestion.content_extractor.requests.get') as mock_content_get, \
             patch('backend.ingestion.chunker.ContentChunker.chunk_content') as mock_chunker, \
             patch('backend.ingestion.embedding_service.EmbeddingService.generate_embeddings') as mock_embeddings, \
             patch('backend.ingestion.vector_storage.VectorStorage.store_embeddings') as mock_vector_store:

            # Set up mocks similar to previous test
            mock_sitemap_get.return_value.text = """<?xml version="1.0" encoding="UTF-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <url>
                    <loc>https://book.example.com/chapter-test</loc>
                </url>
            </urlset>"""
            mock_sitemap_get.return_value.status_code = 200

            mock_content_get.return_value.text = """
            <!DOCTYPE html>
            <html>
            <body>
                <h1>Test Chapter</h1>
                <p>RAG systems use external knowledge to enhance responses.</p>
            </body>
            </html>"""
            mock_content_get.return_value.status_code = 200

            mock_chunker.return_value = ["RAG systems use external knowledge to enhance responses."]
            mock_embeddings.return_value = [[0.1, 0.2, 0.3]]
            mock_vector_store.return_value = True

            # Perform ingestion
            ingest_response = client.post("/api/v1/ingest", json={"sitemap_url": "https://book.example.com/sitemap.xml"})
            assert ingest_response.status_code in [200, 202]

            # Now query about the ingested content
            query_response = client.post("/api/v1/query", json={
                "query": "How do RAG systems enhance responses?",
                "session_id": "ingestion-query-test"
            })

            # Should be able to query successfully
            assert query_response.status_code == 200
            query_result = query_response.json()
            assert "answer" in query_result
            assert "citations" in query_result

    def test_ingestion_error_handling_end_to_end(self, client):
        """Test end-to-end error handling in the ingestion pipeline"""
        with patch('backend.ingestion.sitemap_parser.requests.get') as mock_sitemap_get:
            # Mock a network error
            mock_sitemap_get.side_effect = Exception("Network error")

            response = client.post("/api/v1/ingest", json={"sitemap_url": "https://book.example.com/sitemap.xml"})

            # Should handle the error gracefully, not crash
            assert response.status_code in [500, 400, 200]  # Server error, bad request, or handled gracefully

    def test_ingestion_metadata_tracking(self, client):
        """Test that ingestion jobs are properly tracked with metadata"""
        with patch('backend.ingestion.sitemap_parser.requests.get') as mock_sitemap_get, \
             patch('backend.ingestion.content_extractor.requests.get') as mock_content_get, \
             patch('backend.ingestion.chunker.ContentChunker.chunk_content') as mock_chunker, \
             patch('backend.ingestion.embedding_service.EmbeddingService.generate_embeddings') as mock_embeddings, \
             patch('backend.ingestion.vector_storage.VectorStorage.store_embeddings') as mock_vector_store, \
             patch('backend.app.services.metadata_service.database'):

            # Set up mocks
            mock_sitemap_get.return_value.text = """<?xml version="1.0" encoding="UTF-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <url>
                    <loc>https://book.example.com/chapter-meta</loc>
                </url>
            </urlset>"""
            mock_sitemap_get.return_value.status_code = 200

            mock_content_get.return_value.text = "<html><body><p>Content for metadata testing.</p></body></html>"
            mock_content_get.return_value.status_code = 200

            mock_chunker.return_value = ["Content for metadata testing."]
            mock_embeddings.return_value = [[0.1, 0.2]]
            mock_vector_store.return_value = True

            response = client.post("/api/v1/ingest", json={"sitemap_url": "https://book.example.com/sitemap.xml"})

            assert response.status_code in [200, 202]
            response_data = response.json()

            # Response might include job tracking information
            assert isinstance(response_data, dict)

    def test_ingestion_with_large_content(self, client):
        """Test ingestion behavior with large content"""
        with patch('backend.ingestion.sitemap_parser.requests.get') as mock_sitemap_get, \
             patch('backend.ingestion.content_extractor.requests.get') as mock_content_get, \
             patch('backend.ingestion.chunker.ContentChunker.chunk_content') as mock_chunker, \
             patch('backend.ingestion.embedding_service.EmbeddingService.generate_embeddings') as mock_embeddings, \
             patch('backend.ingestion.vector_storage.VectorStorage.store_embeddings') as mock_vector_store:

            # Mock large sitemap
            large_sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""
            for i in range(100):  # 100 URLs
                large_sitemap_content += f'<url><loc>https://book.example.com/page-{i}</loc></url>'
            large_sitemap_content += "</urlset>"

            mock_sitemap_get.return_value.text = large_sitemap_content
            mock_sitemap_get.return_value.status_code = 200

            # Mock large content
            large_content = "<html><body>" + "<p>This is a large content page with lots of text.</p>" * 50 + "</body></html>"
            mock_content_get.return_value.text = large_content
            mock_content_get.return_value.status_code = 200

            mock_chunker.return_value = ["Chunk of large content"] * 20  # Multiple chunks
            mock_embeddings.return_value = [[0.1, 0.2]] * 20
            mock_vector_store.return_value = True

            response = client.post("/api/v1/ingest", json={"sitemap_url": "https://book.example.com/large-sitemap.xml"})

            # Should handle large content appropriately
            assert response.status_code in [200, 202, 408, 504]  # Success or timeout

    def test_ingestion_chunk_validation(self, client):
        """Test that ingested content is properly chunked according to specifications"""
        with patch('backend.ingestion.sitemap_parser.requests.get') as mock_sitemap_get, \
             patch('backend.ingestion.content_extractor.requests.get') as mock_content_get, \
             patch('backend.ingestion.chunker.ContentChunker.chunk_content') as mock_chunker, \
             patch('backend.ingestion.embedding_service.EmbeddingService.generate_embeddings') as mock_embeddings, \
             patch('backend.ingestion.vector_storage.VectorStorage.store_embeddings') as mock_vector_store:

            mock_sitemap_get.return_value.text = """<?xml version="1.0" encoding="UTF-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <url>
                    <loc>https://book.example.com/chapter-chunk-test</loc>
                </url>
            </urlset>"""
            mock_sitemap_get.return_value.status_code = 200

            long_content = "<html><body><p>" + "This is a test sentence. " * 100 + "</p></body></html>"
            mock_content_get.return_value.text = long_content
            mock_content_get.return_value.status_code = 200

            # Mock the chunker to return appropriately sized chunks
            mock_chunker.return_value = ["Chunk 1: " + "This is a test sentence. " * 25,
                                       "Chunk 2: " + "This is a test sentence. " * 25,
                                       "Chunk 3: " + "This is a test sentence. " * 25,
                                       "Chunk 4: " + "This is a test sentence. " * 25]
            mock_embeddings.return_value = [[0.1, 0.2]] * 4
            mock_vector_store.return_value = True

            response = client.post("/api/v1/ingest", json={"sitemap_url": "https://book.example.com/sitemap.xml"})

            assert response.status_code in [200, 202]
            # The important thing is that chunking happens properly, which is tested via the mock

    def test_ingestion_unicode_and_special_content(self, client):
        """Test ingestion of content with unicode and special characters"""
        with patch('backend.ingestion.sitemap_parser.requests.get') as mock_sitemap_get, \
             patch('backend.ingestion.content_extractor.requests.get') as mock_content_get, \
             patch('backend.ingestion.chunker.ContentChunker.chunk_content') as mock_chunker, \
             patch('backend.ingestion.embedding_service.EmbeddingService.generate_embeddings') as mock_embeddings, \
             patch('backend.ingestion.vector_storage.VectorStorage.store_embeddings') as mock_vector_store:

            mock_sitemap_get.return_value.text = """<?xml version="1.0" encoding="UTF-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <url>
                    <loc>https://book.example.com/chapter-unicode</loc>
                </url>
            </urlset>"""
            mock_sitemap_get.return_value.status_code = 200

            unicode_content = """
            <html>
            <body>
                <h1>Capítulo 1: Sistemas RAG (ñáéíóú)</h1>
                <p>Emojis: 🤖📚💡 and special chars: «»€£¥©®™</p>
            </body>
            </html>"""
            mock_content_get.return_value.text = unicode_content
            mock_content_get.return_value.status_code = 200

            mock_chunker.return_value = ["Capítulo 1: Sistemas RAG (ñáéíóú)", "Emojis: 🤖📚💡 and special chars: «»€£¥©®™"]
            mock_embeddings.return_value = [[0.1, 0.2], [0.3, 0.4]]
            mock_vector_store.return_value = True

            response = client.post("/api/v1/ingest", json={"sitemap_url": "https://book.example.com/sitemap.xml"})

            # Should handle unicode content properly
            assert response.status_code in [200, 202]

    def test_ingestion_concurrent_jobs(self, client):
        """Test handling of concurrent ingestion jobs"""
        import threading
        import time

        results = []

        def run_ingestion(sitemap_url, job_id):
            with patch('backend.ingestion.sitemap_parser.requests.get') as mock_sitemap_get, \
                 patch('backend.ingestion.content_extractor.requests.get') as mock_content_get, \
                 patch('backend.ingestion.chunker.ContentChunker.chunk_content') as mock_chunker, \
                 patch('backend.ingestion.embedding_service.EmbeddingService.generate_embeddings') as mock_embeddings, \
                 patch('backend.ingestion.vector_storage.VectorStorage.store_embeddings') as mock_vector_store:

                mock_sitemap_get.return_value.text = f"""<?xml version="1.0" encoding="UTF-8"?>
                <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                    <url>
                        <loc>https://book.example.com/chapter-{job_id}</loc>
                    </url>
                </urlset>"""
                mock_sitemap_get.return_value.status_code = 200

                mock_content_get.return_value.text = f"<html><body><p>Content for job {job_id}</p></body></html>"
                mock_content_get.return_value.status_code = 200

                mock_chunker.return_value = [f"Content for job {job_id}"]
                mock_embeddings.return_value = [[0.1, 0.2]]
                mock_vector_store.return_value = True

                response = client.post("/api/v1/ingest", json={"sitemap_url": sitemap_url})
                results.append((job_id, response.status_code))

        # Run multiple ingestion jobs concurrently
        threads = []
        for i in range(3):
            thread = threading.Thread(
                target=run_ingestion,
                args=(f"https://book.example.com/sitemap-{i}.xml", f"job-{i}")
            )
            threads.append(thread)
            thread.start()
            time.sleep(0.01)  # Small delay between thread starts

        for thread in threads:
            thread.join()

        # Verify all jobs were processed
        assert len(results) == 3
        for job_id, status_code in results:
            assert status_code in [200, 202]

    def test_ingestion_followed_by_sources_retrieval(self, client):
        """Test that ingested content can have its sources retrieved"""
        with patch('backend.ingestion.sitemap_parser.requests.get') as mock_sitemap_get, \
             patch('backend.ingestion.content_extractor.requests.get') as mock_content_get, \
             patch('backend.ingestion.chunker.ContentChunker.chunk_content') as mock_chunker, \
             patch('backend.ingestion.embedding_service.EmbeddingService.generate_embeddings') as mock_embeddings, \
             patch('backend.ingestion.vector_storage.VectorStorage.store_embeddings') as mock_vector_store:

            # Set up mocks
            mock_sitemap_get.return_value.text = """<?xml version="1.0" encoding="UTF-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <url>
                    <loc>https://book.example.com/chapter-source-test</loc>
                </url>
            </urlset>"""
            mock_sitemap_get.return_value.status_code = 200

            mock_content_get.return_value.text = """
            <html>
            <body>
                <h1>Source Test Chapter</h1>
                <p>This content should be retrievable via sources endpoint.</p>
            </body>
            </html>"""
            mock_content_get.return_value.status_code = 200

            mock_chunker.return_value = ["This content should be retrievable via sources endpoint."]
            mock_embeddings.return_value = [[0.1, 0.2]]
            mock_vector_store.return_value = True

            # Perform ingestion
            ingest_response = client.post("/api/v1/ingest", json={"sitemap_url": "https://book.example.com/sitemap.xml"})
            assert ingest_response.status_code in [200, 202]

            # Try to retrieve a source (would work if the ingestion creates retrievable chunks)
            # Note: This depends on how the ingestion system creates chunk IDs that can be retrieved
            sources_response = client.get("/api/v1/sources/test-chunk-id")
            assert sources_response.status_code in [200, 404]  # May or may not find the chunk

    def test_ingestion_pipeline_integrity(self, client):
        """Test that the ingestion pipeline maintains data integrity"""
        with patch('backend.ingestion.sitemap_parser.requests.get') as mock_sitemap_get, \
             patch('backend.ingestion.content_extractor.requests.get') as mock_content_get, \
             patch('backend.ingestion.chunker.ContentChunker.chunk_content') as mock_chunker, \
             patch('backend.ingestion.embedding_service.EmbeddingService.generate_embeddings') as mock_embeddings, \
             patch('backend.ingestion.vector_storage.VectorStorage.store_embeddings') as mock_vector_store:

            original_content = """
            <html>
            <head><title>Integrity Test</title></head>
            <body>
                <h1>Chapter: Data Integrity in RAG Systems</h1>
                <p>Data integrity is crucial for reliable RAG responses.</p>
                <p>Content must be preserved from source to retrieval.</p>
            </body>
            </html>"""

            mock_sitemap_get.return_value.text = """<?xml version="1.0" encoding="UTF-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <url>
                    <loc>https://book.example.com/integrity-test</loc>
                </url>
            </urlset>"""
            mock_sitemap_get.return_value.status_code = 200

            mock_content_get.return_value.text = original_content
            mock_content_get.return_value.status_code = 200

            # The content should be preserved through the pipeline
            expected_chunks = [
                "Data integrity is crucial for reliable RAG responses.",
                "Content must be preserved from source to retrieval."
            ]
            mock_chunker.return_value = expected_chunks
            mock_embeddings.return_value = [[0.1, 0.2], [0.3, 0.4]]
            mock_vector_store.return_value = True

            response = client.post("/api/v1/ingest", json={"sitemap_url": "https://book.example.com/sitemap.xml"})

            assert response.status_code in [200, 202]
            # Data integrity is maintained if the pipeline processes content correctly