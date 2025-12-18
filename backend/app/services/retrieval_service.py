"""
Qdrant retrieval service for fetching relevant chunks
"""
from typing import List, Dict, Any, Optional
import logging
from ..vector_db import get_qdrant_client
from ..embeddings import generate_embeddings

logger = logging.getLogger(__name__)

class RetrievalService:
    def __init__(self):
        self.client = get_qdrant_client()

    async def retrieve_relevant_chunks(self, query: str, filters: Optional[Dict[str, Any]] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks from Qdrant based on the query
        """
        try:
            logger.info(f"[RetrievalService] Retrieving chunks for query: {query[:50]}...")
            
            # Generate embedding for the query using Cohere
            query_embeddings = generate_embeddings([query])
            query_vector = query_embeddings[0]
            logger.info(f"[RetrievalService] Generated embedding (size: {len(query_vector)})")

            # Search in Qdrant using the query embedding
            search_response = self.client.query_points(
                collection_name="content_chunks",
                query=query_vector,
                limit=limit,
                score_threshold=0.2,  # Lower threshold to get more results
                with_payload=True
            )
            
            # Extract points from response
            if hasattr(search_response, 'points'):
                search_results = search_response.points
            elif isinstance(search_response, list):
                search_results = search_response
            else:
                search_results = []
            
            logger.info(f"[RetrievalService] Retrieved {len(search_results)} chunks from Qdrant")

            # Process the search results into the expected format
            chunks = []
            for result in search_results:
                chunk = {
                    "chunk_id": result.id,
                    "content": result.payload.get("content", ""),
                    "source": "qdrant_retrieved",
                    "module": result.payload.get("module", ""),
                    "chapter": result.payload.get("chapter", ""),
                    "url": result.payload.get("url", ""),
                    "score": result.score
                }
                chunks.append(chunk)

            return chunks

        except Exception as e:
            logger.error(f"[RetrievalService] Error retrieving chunks: {e}")
            import traceback
            traceback.print_exc()
            return []

    async def process_user_selected_text(self, user_text: str, source_url: str = "") -> List[Dict[str, Any]]:
        """
        Process user-selected text for use in the RAG system
        """
        try:
            chunk = {
                "chunk_id": "user_selected_" + str(abs(hash(user_text)))[:8],  # Simple hash-based ID
                "content": user_text,
                "source": "user_selected",  # Mark as user-selected
                "module": "User Selection",
                "chapter": "User Provided",
                "url": source_url,
                "score": 1.0  # Perfect relevance since user provided it
            }

            logger.info(f"Processed user-selected text chunk with {len(user_text)} characters")
            return [chunk]

        except Exception as e:
            logger.error(f"Error processing user-selected text: {e}")
            return []