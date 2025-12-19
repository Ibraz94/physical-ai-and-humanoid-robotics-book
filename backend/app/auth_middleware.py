"""
Better Auth middleware to bridge Node.js Better Auth with FastAPI Python backend.
This middleware handles authentication routes and integrates with the existing API key validation.
"""
import asyncio
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
import subprocess
import sys
import os
from typing import Optional, Dict, Any
import json
import httpx
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration for Better Auth integration
BETTER_AUTH_BASE_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:8000")
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

class BetterAuthBridge:
    """
    Bridge class to handle communication between FastAPI and Better Auth Node.js service.
    This acts as a proxy for authentication endpoints while keeping the main RAG endpoints separate.
    """

    def __init__(self):
        self.better_auth_base_url = BETTER_AUTH_BASE_URL
        self.better_auth_secret = BETTER_AUTH_SECRET

    async def handle_auth_request(self, request: Request) -> Response:
        """
        Handle authentication requests by forwarding them to the Better Auth service.
        This method acts as a proxy for all /auth/* routes.
        """
        # Construct the target URL for Better Auth
        auth_path = request.url.path.replace("/auth", "", 1)
        if auth_path.startswith("//"):
            auth_path = auth_path[1:]

        better_auth_url = f"{self.better_auth_base_url}/api/auth{auth_path}"

        # Prepare headers for the forwarded request
        headers = dict(request.headers)

        # Add authentication if available
        if self.better_auth_secret:
            headers['authorization'] = f"Bearer {self.better_auth_secret}"

        # Prepare the body if present
        body = None
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                body = await request.json()
            except:
                # If JSON parsing fails, get raw body
                body_bytes = await request.body()
                if body_bytes:
                    body = body_bytes.decode('utf-8')

        # Make the request to Better Auth service
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                # Forward the request to Better Auth
                response = await client.request(
                    method=request.method,
                    url=better_auth_url,
                    headers=headers,
                    json=body if isinstance(body, (dict, list)) else None,
                    content=body if isinstance(body, str) and not isinstance(body, (dict, list)) else None
                )

                # Return the response from Better Auth
                return Response(
                    content=response.content,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.headers.get("content-type", "application/json")
                )

            except httpx.RequestError as e:
                # Handle request errors to Better Auth service
                return JSONResponse(
                    status_code=502,
                    content={"detail": f"Error communicating with authentication service: {str(e)}"}
                )
            except Exception as e:
                # Handle other errors
                return JSONResponse(
                    status_code=500,
                    content={"detail": f"Internal error in authentication bridge: {str(e)}"}
                )


# Global instance of the BetterAuthBridge
better_auth_bridge = BetterAuthBridge()


async def better_auth_middleware(request: Request, call_next):
    """
    Middleware function to handle authentication routes separately from RAG endpoints.
    This ensures RAG endpoints remain accessible to anonymous users while
    authentication routes are handled by Better Auth.
    """

    # Check if this is an authentication route
    if request.url.path.startswith("/auth/"):
        # Handle authentication request through Better Auth bridge
        return await better_auth_bridge.handle_auth_request(request)

    # For non-auth routes, continue with the normal flow
    response = await call_next(request)
    return response


def setup_auth_routes(app: FastAPI):
    """
    Set up authentication routes in FastAPI to be handled by the Better Auth bridge.
    """
    @app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
    async def handle_better_auth(request: Request, path: str):
        """
        Catch-all route for Better Auth endpoints.
        All /auth/* routes will be handled by the Better Auth bridge.
        """
        return await better_auth_bridge.handle_auth_request(request)


# Helper functions for session and user management
async def get_current_user_from_session(request: Request) -> Optional[Dict[str, Any]]:
    """
    Extract user information from session if available.
    This is a placeholder implementation - actual implementation would depend on
    how Better Auth stores session information.
    """
    # Check for session cookie
    session_cookie = request.cookies.get("better-auth-session")

    if not session_cookie:
        return None

    # In a real implementation, this would validate the session with Better Auth
    # For now, return a placeholder structure
    try:
        # This would normally call Better Auth's session validation API
        # Placeholder implementation
        return {
            "id": "placeholder_user_id",
            "email": "placeholder@example.com",
            "session_valid": True
        }
    except Exception:
        return None


async def require_auth_middleware(request: Request, call_next):
    """
    Middleware to require authentication for specific routes.
    Unlike the main auth middleware which routes /auth/* to Better Auth,
    this middleware validates that a user is authenticated for protected routes.
    """
    # List of routes that require authentication
    protected_routes = [
        "/api/v1/profile",
        "/api/v1/settings",
        "/api/v1/user-data"
    ]

    # Check if the current path requires authentication
    requires_auth = any(request.url.path.startswith(route) for route in protected_routes)

    if requires_auth:
        current_user = await get_current_user_from_session(request)
        if not current_user or not current_user.get("session_valid"):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authentication required"}
            )

    # Continue with the normal request flow
    response = await call_next(request)
    return response