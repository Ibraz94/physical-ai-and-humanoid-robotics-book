"""
Qdrant client setup for vector database operations
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional, Dict, Any
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Global Qdrant client instance
_qdrant_client: Optional[QdrantClient] = None

def init_qdrant_client() -> QdrantClient:
    """
    Initialize the Qdrant client
    """
    global _qdrant_client

    if _qdrant_client is None:
        try:
            if settings.qdrant_api_key:
                _qdrant_client = QdrantClient(
                    url=settings.qdrant_url,
                    api_key=settings.qdrant_api_key,
                    timeout=10
                )
            else:
                # For local development without API key
                _qdrant_client = QdrantClient(
                    url=settings.qdrant_url,
                    timeout=10
                )

            logger.info("Qdrant client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {e}")
            raise

    return _qdrant_client

def get_qdrant_client() -> QdrantClient:
    """
    Get the Qdrant client instance
    """
    if _qdrant_client is None:
        return init_qdrant_client()

    return _qdrant_client

async def ensure_collection_exists(
    collection_name: str,
    vector_size: int = 1536,  # Default size for OpenAI embeddings, adjust as needed
    distance: models.Distance = models.Distance.COSINE
) -> bool:
    """
    Ensure that a collection exists in Qdrant, create it if it doesn't
    """
    client = get_qdrant_client()

    try:
        # Try to get collection info to check if it exists
        client.get_collection(collection_name)
        logger.info(f"Collection '{collection_name}' already exists")
        return True
    except Exception:
        # Collection doesn't exist, create it
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=distance
            )
        )
        logger.info(f"Created collection '{collection_name}'")
        return False