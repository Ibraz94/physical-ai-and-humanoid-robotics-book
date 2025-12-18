"""
Embedding generation service using Cohere
"""
from typing import List, Dict, Any
from ..app.embeddings import generate_embeddings
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        pass

    async def generate_embeddings_for_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate embeddings for a list of content chunks
        """
        try:
            if not chunks:
                logger.info("No chunks to generate embeddings for")
                return []

            # Extract content from chunks for embedding generation
            contents = [chunk["content"] for chunk in chunks]

            logger.info(f"Generating embeddings for {len(contents)} chunks")

            # Generate embeddings using Cohere
            embeddings = generate_embeddings(contents)

            # Attach embeddings to chunks
            updated_chunks = []
            for i, chunk in enumerate(chunks):
                updated_chunk = chunk.copy()
                updated_chunk["embedding"] = embeddings[i]
                updated_chunks.append(updated_chunk)

            logger.info(f"Successfully generated embeddings for {len(updated_chunks)} chunks")
            return updated_chunks

        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []

    async def generate_embedding_for_content(self, content: str) -> List[float]:
        """
        Generate embedding for a single content string
        """
        try:
            logger.info(f"Generating embedding for content ({len(content)} characters)")

            # Generate embedding using Cohere
            embeddings = generate_embeddings([content])
            embedding = embeddings[0]  # Get the first (and only) embedding

            logger.info(f"Generated embedding with {len(embedding)} dimensions")
            return embedding

        except Exception as e:
            logger.error(f"Error generating embedding for content: {e}")
            return []