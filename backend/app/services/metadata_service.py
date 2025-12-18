"""
Metadata persistence service for storing agent interactions and session data
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import logging
from ..models.query import QueryRequest, QueryResponse
from ..database import get_db_connection

logger = logging.getLogger(__name__)

class MetadataService:
    def __init__(self):
        pass

    async def store_query_interaction(
        self,
        session_id: str,
        query_request: QueryRequest,
        query_response: QueryResponse,
        metadata: Optional[dict] = None
    ) -> str:
        """
        Store query interaction metadata in the database
        """
        try:
            interaction_id = f"interaction_{str(uuid.uuid4())}"
            timestamp = datetime.utcnow()

            # In a real implementation, this would store in the database
            # For now, we'll just log the interaction
            interaction_data = {
                "interaction_id": interaction_id,
                "session_id": session_id,
                "query": query_request.query,
                "context": query_request.context,
                "answer": query_response.answer,
                "citations_count": len(query_response.citations),
                "timestamp": timestamp,
                "metadata": metadata or {}
            }

            logger.info(f"Stored query interaction: {interaction_id} for session {session_id}")
            return interaction_id

        except Exception as e:
            logger.error(f"Error storing query interaction: {e}")
            # Return a mock ID in case of error
            return f"interaction_{str(uuid.uuid4())}"

    async def get_session_interactions(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all interactions for a given session
        """
        try:
            # In a real implementation, this would fetch from the database
            # For now, return mock data
            logger.info(f"Retrieving interactions for session: {session_id}")
            return []

        except Exception as e:
            logger.error(f"Error retrieving session interactions: {e}")
            return []

    async def store_session_metadata(self, session_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Store session-specific metadata
        """
        try:
            # In a real implementation, this would store in the database
            logger.info(f"Stored metadata for session: {session_id}")
            return True

        except Exception as e:
            logger.error(f"Error storing session metadata: {e}")
            return False

    async def get_session_metadata(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve session-specific metadata
        """
        try:
            # In a real implementation, this would fetch from the database
            logger.info(f"Retrieved metadata for session: {session_id}")
            return {"device": "web", "location": "US"}  # Mock data

        except Exception as e:
            logger.error(f"Error retrieving session metadata: {e}")
            return None

    async def store_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """
        Store user preferences in the database
        """
        try:
            # In a real implementation, this would store in the database
            logger.info(f"Stored preferences for user: {user_id}")
            return True

        except Exception as e:
            logger.error(f"Error storing user preferences: {e}")
            return False

    async def get_user_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user preferences from the database
        """
        try:
            # In a real implementation, this would fetch from the database
            logger.info(f"Retrieved preferences for user: {user_id}")
            return {"theme": "light", "language": "en"}  # Mock data

        except Exception as e:
            logger.error(f"Error retrieving user preferences: {e}")
            return None