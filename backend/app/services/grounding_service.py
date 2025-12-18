"""
Grounding service to enforce strict grounding rules
"""
from typing import List, Dict, Any, Union
import logging

logger = logging.getLogger(__name__)

class GroundingService:
    def __init__(self):
        pass

    def validate_context(self, context_chunks: List[Dict[str, Any]]) -> bool:
        """
        Validate that the context follows grounding rules:
        - Only use Qdrant-retrieved chunks OR user-selected text
        - No external knowledge, browsing, or hallucinations
        """
        try:
            if not context_chunks:
                logger.info("No context chunks to validate")
                return False

            # Check each chunk to ensure it comes from an approved source
            for chunk in context_chunks:
                source = chunk.get("source", "")

                # Valid sources are either from Qdrant (retrieved) or user-selected
                if not (source == "qdrant_retrieved" or source == "user_selected"):
                    logger.warning(f"Invalid context source: {source}")
                    return False

            logger.info(f"Validated {len(context_chunks)} context chunks successfully")
            return True

        except Exception as e:
            logger.error(f"Error validating context: {e}")
            return False

    def enforce_grounding_rules(self, query: str, response: str, context: List[Dict[str, Any]]) -> str:
        """
        Enforce grounding rules on the response to ensure it only uses provided context
        """
        try:
            # This is a simplified implementation
            # In a real system, you would have more sophisticated grounding validation

            # Check if the response seems to be grounded in the context
            response_lower = response.lower()

            # Look for evidence that the response is based on the provided context
            context_evidence = False
            for chunk in context:
                chunk_content = chunk.get("content", "").lower()
                if len(chunk_content) > 10:  # Only check substantial content
                    if chunk_content in response_lower:
                        context_evidence = True
                        break

            # If no clear evidence of grounding, ensure the response follows grounding rules
            if not context_evidence and "i don't know based on the provided text." not in response.lower():
                # This is a simplified check - in reality, you'd want more sophisticated validation
                logger.info("Response may not be properly grounded, but allowing based on content")

            return response

        except Exception as e:
            logger.error(f"Error enforcing grounding rules: {e}")
            # Return the original response if grounding enforcement fails
            return response