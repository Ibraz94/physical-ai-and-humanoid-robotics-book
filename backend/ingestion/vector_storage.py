"""
Qdrant storage service for storing embeddings
"""
from typing import List, Dict, Any
from qdrant_client.http import models
from ..app.vector_db import get_qdrant_client, ensure_collection_exists
import logging

logger = logging.getLogger(__name__)

class VectorStorageService:
    def __init__(self, collection_name: str = "content_chunks"):
        self.client = get_qdrant_client()
        self.collection_name = collection_name

    async def initialize_storage(self):
        """
        Initialize the storage by ensuring the collection exists
        """
        try:
            # Ensure the collection exists with appropriate vector size
            # Using 1024 as a common size for Cohere embeddings (adjust as needed)
            await ensure_collection_exists(
                collection_name=self.collection_name,
                vector_size=1024,  # Standard size for Cohere embeddings
                distance=models.Distance.COSINE
            )
            logger.info(f"Vector storage initialized for collection: {self.collection_name}")

        except Exception as e:
            logger.error(f"Error initializing vector storage: {e}")
            raise

    async def store_chunks(self, chunks: List[Dict[str, Any]]) -> bool:
        """
        Store content chunks with their embeddings in Qdrant
        """
        try:
            if not chunks:
                logger.info("No chunks to store")
                return True

            logger.info(f"Storing {len(chunks)} chunks in Qdrant collection: {self.collection_name}")

            # Prepare points for upsert
            points = []
            for chunk in chunks:
                # Ensure we have an embedding
                if "embedding" not in chunk:
                    logger.warning(f"Chunk {chunk.get('chunk_id', 'unknown')} missing embedding, skipping")
                    continue

                point = models.PointStruct(
                    id=chunk["chunk_id"],
                    vector=chunk["embedding"],
                    payload={
                        "content": chunk["content"],
                        "source_url": chunk["source_url"],
                        "title": chunk.get("title", ""),
                        "module": chunk.get("module", ""),
                        "chapter": chunk.get("chapter", ""),
                        "anchor": chunk.get("anchor", ""),
                        "token_count": chunk.get("token_count", 0),
                        "created_at": chunk.get("created_at", "")
                    }
                )
                points.append(point)

            # Upsert the points into Qdrant
            if points:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )

                logger.info(f"Successfully stored {len(points)} chunks in Qdrant")
                return True
            else:
                logger.info("No points with embeddings to store")
                return True

        except Exception as e:
            logger.error(f"Error storing chunks in Qdrant: {e}")
            return False

    async def store_chunk(self, chunk: Dict[str, Any]) -> bool:
        """
        Store a single content chunk with its embedding in Qdrant
        """
        try:
            logger.info(f"Storing chunk {chunk.get('chunk_id', 'unknown')} in Qdrant")

            # Ensure we have an embedding
            if "embedding" not in chunk:
                logger.error(f"Chunk {chunk.get('chunk_id', 'unknown')} missing embedding")
                return False

            # Prepare the point
            point = models.PointStruct(
                id=chunk["chunk_id"],
                vector=chunk["embedding"],
                payload={
                    "content": chunk["content"],
                    "source_url": chunk["source_url"],
                    "title": chunk.get("title", ""),
                    "module": chunk.get("module", ""),
                    "chapter": chunk.get("chapter", ""),
                    "anchor": chunk.get("anchor", ""),
                    "token_count": chunk.get("token_count", 0),
                    "created_at": chunk.get("created_at", "")
                }
            )

            # Upsert the point into Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            logger.info(f"Successfully stored chunk {chunk['chunk_id']} in Qdrant")
            return True

        except Exception as e:
            logger.error(f"Error storing chunk in Qdrant: {e}")
            return False

    async def delete_chunk(self, chunk_id: str) -> bool:
        """
        Delete a chunk from Qdrant by its ID
        """
        try:
            logger.info(f"Deleting chunk {chunk_id} from Qdrant")

            # Delete the point from Qdrant
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[chunk_id]
                )
            )

            logger.info(f"Successfully deleted chunk {chunk_id} from Qdrant")
            return True

        except Exception as e:
            logger.error(f"Error deleting chunk from Qdrant: {e}")
            return False

    async def search_chunks(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar chunks based on embedding similarity
        """
        try:
            logger.info(f"Searching for similar chunks (limit: {limit})")

            # Search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True,
                with_vectors=False
            )

            # Process results
            results = []
            for result in search_results:
                chunk_data = {
                    "chunk_id": result.id,
                    "content": result.payload.get("content", ""),
                    "source_url": result.payload.get("source_url", ""),
                    "title": result.payload.get("title", ""),
                    "module": result.payload.get("module", ""),
                    "chapter": result.payload.get("chapter", ""),
                    "anchor": result.payload.get("anchor", ""),
                    "score": result.score
                }
                results.append(chunk_data)

            logger.info(f"Found {len(results)} similar chunks")
            return results

        except Exception as e:
            logger.error(f"Error searching for chunks in Qdrant: {e}")
            return []

    async def verify_ingested_content(self, chunk_ids: List[str]) -> Dict[str, bool]:
        """
        Verify that ingested content is properly stored and retrievable
        """
        try:
            logger.info(f"Verifying {len(chunk_ids)} ingested chunks")

            verification_results = {}

            for chunk_id in chunk_ids:
                try:
                    # Try to retrieve the chunk
                    records = self.client.retrieve(
                        collection_name=self.collection_name,
                        ids=[chunk_id],
                        with_payload=True,
                        with_vectors=False
                    )

                    # Check if the chunk exists and has proper content
                    if records and len(records) > 0:
                        record = records[0]
                        payload = record.payload

                        # Verify that the payload contains expected fields
                        has_content = bool(payload.get("content", ""))
                        has_source = bool(payload.get("source_url", ""))

                        verification_results[chunk_id] = has_content and has_source
                    else:
                        verification_results[chunk_id] = False

                except Exception as e:
                    logger.warning(f"Error verifying chunk {chunk_id}: {e}")
                    verification_results[chunk_id] = False

            success_count = sum(1 for verified in verification_results.values() if verified)
            logger.info(f"Verification complete: {success_count}/{len(chunk_ids)} chunks verified successfully")
            return verification_results

        except Exception as e:
            logger.error(f"Error verifying ingested content: {e}")
            return {}

    async def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the stored content
        """
        try:
            # Get collection info
            collection_info = self.client.get_collection(self.collection_name)

            stats = {
                "total_chunks": collection_info.points_count,
                "collection_name": self.collection_name,
                "vectors_count": collection_info.vectors_count,
            }

            logger.info(f"Storage stats: {stats}")
            return stats

        except Exception as e:
            logger.error(f"Error getting storage stats: {e}")
            return {}