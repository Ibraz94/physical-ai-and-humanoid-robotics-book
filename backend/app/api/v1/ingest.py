"""
API endpoint for triggering content ingestion (POST /ingest)
"""
from fastapi import APIRouter, HTTPException
import logging
from typing import Optional

from ...models import IngestionRequest, IngestionResponse
from ...services.ingestion_service import IngestionService
from ...utils import get_logger

router = APIRouter()
logger = get_logger(__name__)
ingestion_service = IngestionService()

@router.post("/ingest", response_model=IngestionResponse, summary="Trigger content ingestion into the knowledge base")
async def trigger_ingestion(ingestion_request: IngestionRequest):
    """
    Start the process of ingesting new content into the knowledge base
    """
    request_id = f"req_{abs(hash(str(ingestion_request.sitemap_url or '') + str(len(ingestion_request.urls or [])))) % 1000000}"
    logger.info(f"[{request_id}] Received ingestion request")

    try:
        # Validate the request
        if not ingestion_request.sitemap_url and not ingestion_request.urls:
            logger.warning(f"[{request_id}] Invalid ingestion request: no sitemap_url or urls provided")
            raise HTTPException(
                status_code=400,
                detail="Either sitemap_url or urls must be provided"
            )

        # Process the ingestion request
        job_id = await ingestion_service.process_ingestion_request(ingestion_request)

        response = IngestionResponse(
            status="started",
            job_id=job_id,
            message="Ingestion process started successfully"
        )

        logger.info(f"[{request_id}] Ingestion started with job ID: {job_id}")
        return response

    except HTTPException as e:
        logger.warning(f"[{request_id}] HTTP error {e.status_code}: {e.detail}")
        raise

    except Exception as e:
        logger.error(f"[{request_id}] Unexpected error during ingestion: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")