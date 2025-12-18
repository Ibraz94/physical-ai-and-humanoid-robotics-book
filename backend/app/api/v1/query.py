"""
API endpoint for processing queries (POST /query)
"""
from fastapi import APIRouter, HTTPException
import logging

from ...models.query import QueryRequest, QueryResponse
from ...services.agent_service import AgentService
from ...utils import get_logger
from ...utils.exceptions import ContextInsufficientException

router = APIRouter()
logger = get_logger(__name__)
agent_service = AgentService()

@router.post("/query", response_model=QueryResponse, summary="Submit a query to the RAG system")
async def process_query(query_request: QueryRequest):
    """
    Process a user query against the knowledge base and return a grounded response
    """
    request_id = f"req_{abs(hash(str(query_request.query) + str(query_request.session_id or ''))) % 1000000}"
    logger.info(f"[{request_id}] Received query: {query_request.query[:100]}...")

    try:
        # Validate the query
        if not query_request.query or len(query_request.query.strip()) == 0:
            logger.warning(f"[{request_id}] Invalid query: empty query")
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Process the query using the agent service
        response = await agent_service.process_query(query_request)

        logger.info(f"[{request_id}] Query processed successfully, response length: {len(response.answer)}")
        return response

    except ContextInsufficientException as e:
        # Return the specific "I don't know" response when context is insufficient
        response = QueryResponse(
            answer=e.message,
            citations=[],
            session_id=query_request.session_id
        )
        logger.info(f"[{request_id}] Returning insufficient context response")
        return response

    except HTTPException as e:
        logger.warning(f"[{request_id}] HTTP error {e.status_code}: {e.detail}")
        raise

    except Exception as e:
        logger.error(f"[{request_id}] Unexpected error processing query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")