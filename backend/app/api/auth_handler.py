"""
Better Auth API Handler
Handles the integration between Better Auth (Node.js) and FastAPI (Python)
This module creates a bridge that allows the Node.js Better Auth service to work
with the Python FastAPI backend while maintaining separation between auth and RAG functionality.
"""

import os
import httpx
from fastapi import Request, Response, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import asyncio
import logging

logger = logging.getLogger(__name__)

# Get Better Auth configuration from environment
BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:8001")
BETTER_AUTH_COOKIE_NAME = os.getenv("BETTER_AUTH_COOKIE_NAME", "better-auth-session")

router = APIRouter(prefix="/api/auth")

class BetterAuthProxy:
    """
    Proxy class to forward authentication requests to the Better Auth Node.js service
    while maintaining separation from RAG functionality.
    """

    def __init__(self):
        self.better_auth_url = BETTER_AUTH_URL
        self.client = httpx.AsyncClient(timeout=30.0)

    async def forward_request(self, request: Request, path: str) -> Response:
        """
        Forward the incoming request to Better Auth service and return its response

        Args:
            request: The original FastAPI request
            path: The auth endpoint path to forward to Better Auth

        Returns:
            Response from Better Auth service
        """
        # Construct the target URL for Better Auth
        target_url = f"{self.better_auth_url}{path}"

        # Prepare headers (excluding host header which causes issues)
        headers = dict(request.headers)
        if 'host' in headers:
            # Replace host header with the Better Auth host
            headers['host'] = f"{os.getenv('BETTER_AUTH_HOST', 'localhost')}:{os.getenv('BETTER_AUTH_PORT', '8001')}"

        # Prepare query parameters
        query_params = str(request.url.query) if request.url.query else ""
        if query_params:
            target_url += f"?{query_params}"

        try:
            # Make the request to Better Auth
            better_auth_response = await self.client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=await request.body(),
            )

            # Create and return the response with Better Auth's content
            response = Response(
                status_code=better_auth_response.status_code,
                content=better_auth_response.content,
                headers=dict(better_auth_response.headers),
            )

            return response

        except httpx.RequestError as e:
            logger.error(f"Error forwarding request to Better Auth: {str(e)}")
            logger.error(f"Target URL was: {target_url}")
            logger.error(f"Better Auth URL configured: {self.better_auth_url}")
            raise HTTPException(
                status_code=502,
                detail=f"Unable to connect to authentication service: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error in Better Auth proxy: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal error in authentication service: {str(e)}"
            )

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Global instance of the proxy
better_auth_proxy = BetterAuthProxy()


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def handle_better_auth(request: Request, path: str):
    """
    Catch-all route for Better Auth endpoints.
    All /api/auth/* routes will be forwarded to the Better Auth service.

    Args:
        request: The incoming FastAPI request
        path: The remaining path after /api/auth/

    Returns:
        Response from Better Auth service
    """
    # Construct the full path for Better Auth
    full_path = f"/api/auth/{path}"

    # Log the request for debugging
    logger.info(f"Forwarding auth request: {request.method} {full_path}")

    # Forward the request to Better Auth service
    response = await better_auth_proxy.forward_request(request, full_path)

    return response


# Function to get the current user session from Better Auth
async def get_current_user_session(request: Request) -> Optional[dict]:
    """
    Get the current user session from Better Auth.
    This function calls the Better Auth session endpoint to verify if a user is authenticated.

    Args:
        request: The incoming FastAPI request (with session cookie)

    Returns:
        User session data if authenticated, None otherwise
    """
    try:
        # Get cookies from the request
        cookies = {}
        for key, value in request.cookies.items():
            cookies[key] = value

        # Make a request to Better Auth's session endpoint
        session_response = await better_auth_proxy.client.get(
            f"{BETTER_AUTH_URL}/api/auth/session",
            cookies=cookies,
        )

        if session_response.status_code == 200:
            session_data = session_response.json()
            return session_data
        else:
            logger.debug(f"No valid session found: {session_response.status_code}")
            return None

    except Exception as e:
        logger.warning(f"Error getting session from Better Auth: {str(e)}")
        return None


# Function to initialize the Better Auth handler (call this during app startup)
async def initialize_auth_handler():
    """
    Initialize the Better Auth handler.
    This should be called during application startup.
    """
    logger.info("Initializing Better Auth handler...")
    # Any initialization logic for the auth handler would go here
    # For now, we just log that initialization occurred


# Function to cleanup the Better Auth handler (call this during app shutdown)
async def cleanup_auth_handler():
    """
    Cleanup the Better Auth handler.
    This should be called during application shutdown.
    """
    logger.info("Cleaning up Better Auth handler...")
    await better_auth_proxy.close()


# Include the router in the main app
def get_auth_router():
    """
    Get the auth router to be included in the main FastAPI app.
    This function returns the router with all auth routes configured.
    """
    return router