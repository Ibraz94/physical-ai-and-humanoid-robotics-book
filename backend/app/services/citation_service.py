"""
Citation service to generate proper citations for responses
"""
from typing import List, Dict, Any
from ..models.source import SourceReference
import logging

logger = logging.getLogger(__name__)

class CitationService:
    def __init__(self):
        pass

    def generate_citations(self, context_chunks: List[Dict[str, Any]]) -> List[SourceReference]:
        """
        Generate citations based on the context chunks used to answer the query
        """
        try:
            citations = []

            for chunk in context_chunks:
                # Create a SourceReference from the chunk data
                citation = SourceReference(
                    chunk_id=chunk.get("chunk_id", ""),
                    module=chunk.get("module", "Unknown"),
                    chapter=chunk.get("chapter", "Unknown"),
                    anchor=chunk.get("anchor", ""),
                    url=chunk.get("url", "")
                )
                citations.append(citation)

            logger.info(f"Generated {len(citations)} citations")
            return citations

        except Exception as e:
            logger.error(f"Error generating citations: {e}")
            return []

    def validate_citations(self, citations: List[SourceReference]) -> bool:
        """
        Validate that citations are properly formatted and contain required information
        """
        try:
            for citation in citations:
                if not citation.chunk_id:
                    logger.warning("Citation missing chunk_id")
                    return False

                if not citation.url:
                    logger.warning("Citation missing URL")
                    return False

            logger.info(f"Validated {len(citations)} citations successfully")
            return True

        except Exception as e:
            logger.error(f"Error validating citations: {e}")
            return False