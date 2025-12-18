"""
API endpoint for retrieving source information (GET /sources/{chunk_id})
"""
from fastapi import APIRouter, HTTPException
import logging

from ...models import SourceReference
from ...services.chunk_service import ChunkService
from ...utils import get_logger

router = APIRouter()
logger = get_logger(__name__)
chunk_service = ChunkService()

@router.get("/sources/{chunk_id}", response_model=SourceReference, summary="Get source information for a chunk")
async def get_source_info(chunk_id: str):
    """
    Retrieve the source information for a specific content chunk
    """
    request_id = f"req_{abs(hash(chunk_id)) % 1000000}"
    logger.info(f"[{request_id}] Received request for source info for chunk_id: {chunk_id}")

    try:
        # Use the chunk service to get chunk information
        chunk_data = await chunk_service.get_chunk_by_id(chunk_id)

        if chunk_data is None:
            logger.warning(f"[{request_id}] Chunk not found: {chunk_id}")
            raise HTTPException(status_code=404, detail="Chunk not found")

        # Create and return the source reference
        source_ref = SourceReference(
            chunk_id=chunk_data["chunk_id"],
            module=chunk_data["module"],
            chapter=chunk_data["chapter"],
            anchor=chunk_data["anchor"],
            url=chunk_data["source_url"]
        )

        logger.info(f"[{request_id}] Found source info for chunk_id: {chunk_id}")
        return source_ref

    except HTTPException as e:
        logger.warning(f"[{request_id}] HTTP error {e.status_code}: {e.detail}")
        raise

    except Exception as e:
        logger.error(f"[{request_id}] Unexpected error retrieving source info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")