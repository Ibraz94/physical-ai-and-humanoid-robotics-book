"""
API endpoint for processing user-selected text (POST /select)
"""
from fastapi import APIRouter, HTTPException
import logging

from ...models import SelectedTextRequest, SelectedTextResponse
from ...utils import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/select", response_model=SelectedTextResponse, summary="Submit user-selected text for the RAG system")
async def process_selected_text(selected_text_request: SelectedTextRequest):
    """
    Process user-selected text for use in the RAG system
    """
    request_id = f"req_{abs(hash(str(selected_text_request.text) + str(selected_text_request.source_url))) % 1000000}"
    logger.info(f"[{request_id}] Received selected text request with {len(selected_text_request.text)} characters")

    try:
        # Validate the request
        if not selected_text_request.text or len(selected_text_request.text.strip()) == 0:
            logger.warning(f"[{request_id}] Invalid request: empty selected text")
            raise HTTPException(status_code=400, detail="Selected text cannot be empty")

        if not selected_text_request.source_url:
            logger.warning(f"[{request_id}] Invalid request: missing source URL")
            raise HTTPException(status_code=400, detail="Source URL is required")

        # Process the selected text (for now, just validate and acknowledge)
        # In a full implementation, this would involve storing the text for later use
        processed_text_id = f"txt_{abs(hash(selected_text_request.text)) % 1000000}"

        response = SelectedTextResponse(
            status="success",
            message="Selected text processed successfully",
            processed_text_id=processed_text_id
        )

        logger.info(f"[{request_id}] Selected text processed successfully with ID: {processed_text_id}")
        return response

    except HTTPException as e:
        logger.warning(f"[{request_id}] HTTP error {e.status_code}: {e.detail}")
        raise

    except Exception as e:
        logger.error(f"[{request_id}] Unexpected error processing selected text: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")