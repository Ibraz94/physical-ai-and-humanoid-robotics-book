"""
Better Auth Integration for FastAPI Backend

This module provides the integration between Better Auth (Node.js) and FastAPI (Python)
while maintaining separation between authentication and RAG functionality.
The implementation ensures that RAG endpoints remain accessible to anonymous users.
"""

import os
import httpx
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Get Better Auth configuration from environment
BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:8001")
BETTER_AUTH_COOKIE_NAME = os.getenv("BETTER_AUTH_COOKIE_NAME", "better-auth-session")


class BetterAuthIntegration:
    """
    Main integration class for Better Auth with FastAPI.
    Handles session validation, user lookup, and communication with Better Auth service.
    """

    def __init__(self):
        self.better_auth_url = BETTER_AUTH_URL
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    async def get_session(self, request: Request) -> Optional[Dict[str, Any]]:
        """
        Get the current session from Better Auth service.

        Args:
            request: The incoming FastAPI request with session cookies

        Returns:
            Session data if valid, None otherwise
        """
        try:
            # Extract cookies from the request
            cookies = {}
            for key, value in request.cookies.items():
                cookies[key] = value

            # Make request to Better Auth session endpoint
            response = await self.client.get(
                f"{self.better_auth_url}/api/auth/session",
                cookies=cookies,
            )

            if response.status_code == 200:
                session_data = response.json()
                return session_data
            else:
                logger.debug(f"No valid session found: {response.status_code}")
                return None

        except Exception as e:
            logger.warning(f"Error getting session from Better Auth: {str(e)}")
            return None

    async def validate_endpoint_access(self, request: Request, endpoint_path: str) -> bool:
        """
        Determine if an endpoint requires authentication or can be accessed anonymously.

        Args:
            request: The incoming request
            endpoint_path: The path of the endpoint being accessed

        Returns:
            True if access is allowed (either authenticated or public), False otherwise
        """
        # Define public RAG endpoints that should remain accessible to anonymous users
        public_endpoints = [
            "/api/v1/query",
            "/api/v1/select",
            "/api/v1/sources",
            "/api/v1/ingest/status",  # Status endpoint might also be public
        ]

        # Check if this is a public RAG endpoint
        for public_endpoint in public_endpoints:
            if endpoint_path.startswith(public_endpoint):
                return True  # Always allow access to public RAG endpoints

        # For authentication endpoints, allow access (they'll be handled by Better Auth service)
        if endpoint_path.startswith("/api/auth"):
            return True

        # For all other endpoints, check if user is authenticated
        session = await self.get_session(request)
        return session is not None

    async def forward_auth_request(self, request: Request, path: str) -> Response:
        """
        Forward authentication requests to the Better Auth service.

        Args:
            request: The incoming FastAPI request
            path: The auth endpoint path to forward

        Returns:
            Response from Better Auth service
        """
        # Construct the target URL for Better Auth
        target_url = f"{self.better_auth_url}{path}"

        # Prepare headers (excluding host to avoid issues)
        headers = dict(request.headers)
        if 'host' in headers:
            # Replace host header with the Better Auth host
            better_auth_host = os.getenv('BETTER_AUTH_HOST', 'localhost')
            better_auth_port = os.getenv('BETTER_AUTH_PORT', '8001')
            headers['host'] = f"{better_auth_host}:{better_auth_port}"

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
                content=await request.body() if request.method in ["POST", "PUT", "PATCH"] else None,
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
            raise HTTPException(
                status_code=502,
                detail=f"Unable to connect to authentication service: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error in Better Auth proxy: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal error in authentication service"
            )


# Global instance of the Better Auth integration
better_auth = BetterAuthIntegration()


async def get_current_user(request: Request) -> Optional[Dict[str, Any]]:
    """
    Get the current authenticated user from the session.

    Args:
        request: The incoming FastAPI request

    Returns:
        User data if authenticated, None otherwise
    """
    session = await better_auth.get_session(request)

    # Log authentication event while preserving privacy
    if session:
        user_id = session.get('user', {}).get('id', 'unknown')
        logger.info(f"User session retrieved for user_id: {user_id[:8]}... (truncated for privacy)")
    else:
        logger.debug("No valid session found for request")

    return session


async def is_endpoint_accessible(request: Request, endpoint_path: str) -> bool:
    """
    Check if the current request can access the specified endpoint.

    Args:
        request: The incoming request
        endpoint_path: The path of the endpoint to access

    Returns:
        True if access is allowed, False otherwise
    """
    return await better_auth.validate_endpoint_access(request, endpoint_path)


# Function to initialize the auth integration
async def initialize_auth():
    """Initialize the Better Auth integration."""
    logger.info("Initializing Better Auth integration...")
    # Any initialization logic would go here
    # Currently, the global instance is already created


# Function to cleanup the auth integration
async def cleanup_auth():
    """Cleanup the Better Auth integration."""
    logger.info("Cleaning up Better Auth integration...")
    await better_auth.close()