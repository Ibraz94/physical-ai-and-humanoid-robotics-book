"""
Cohere client setup for embedding generation
"""
import cohere
from typing import List, Optional
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Global Cohere client instance
_cohere_client: Optional[cohere.Client] = None

def init_cohere_client() -> cohere.Client:
    """
    Initialize the Cohere client
    """
    global _cohere_client

    if _cohere_client is None:
        try:
            _cohere_client = cohere.Client(api_key=settings.cohere_api_key)
            logger.info("Cohere client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Cohere client: {e}")
            raise

    return _cohere_client

def get_cohere_client() -> cohere.Client:
    """
    Get the Cohere client instance
    """
    if _cohere_client is None:
        return init_cohere_client()

    return _cohere_client

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using Cohere
    """
    client = get_cohere_client()

    try:
        response = client.embed(
            texts=texts,
            model='embed-english-v3.0',  # Using Cohere's latest embedding model
            input_type="search_document"  # Specify the input type for better results
        )

        return [embedding for embedding in response.embeddings]
    except Exception as e:
        logger.error(f"Failed to generate embeddings: {e}")
        raise