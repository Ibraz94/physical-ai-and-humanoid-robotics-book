"""
Custom middleware for security and request processing
"""
from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import ClientDisconnect
import time
import logging
from .security import APIKeyValidator
from .services.metrics_service import MetricsService

logger = logging.getLogger(__name__)
metrics_service = MetricsService()

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Start timing the request
        start_time = time.time()

        # Add security headers
        response = await call_next(request)

        # Add security headers to the response
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # Calculate duration for metrics
        duration = time.time() - start_time

        # Record metrics
        status_code = response.status_code
        endpoint = request.url.path
        await metrics_service.record_api_call(endpoint, duration, status_code)

        return response

class APIKeyValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip validation for OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)
            
        # Skip validation for health checks, root endpoint, and auth endpoints
        if request.url.path in ["/", "/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Skip validation for all auth endpoints (Better Auth handles its own authentication)
        if request.url.path.startswith("/api/auth") or request.url.path.startswith("/auth"):
            return await call_next(request)

        # Define public RAG endpoints that should remain accessible to anonymous users
        public_endpoints = [
            "/api/v1/query",
            "/api/v1/select",
            "/api/v1/sources",  # These might also be public depending on requirements
        ]

        # Check if this is a public RAG endpoint accessed via GET/POST/PUT/DELETE
        is_public_rag_endpoint = any(
            request.url.path.startswith(endpoint) for endpoint in public_endpoints
        )

        # Skip API key validation for public RAG endpoints
        if is_public_rag_endpoint and request.method in ["GET", "POST", "PUT", "DELETE"]:
            return await call_next(request)

        # Validate API key for protected endpoints
        auth_header = request.headers.get("Authorization")

        if auth_header:
            # Extract the token part after "Bearer "
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
                # Validate the token
                try:
                    is_valid = await APIKeyValidator.validate_api_key(type('obj', (object,), {'credentials': token})())
                    if not is_valid:
                        return JSONResponse(
                            status_code=401,
                            content={"detail": "Invalid API key"}
                        )
                except HTTPException:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Invalid API key"}
                    )
            else:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid Authorization header format, use 'Bearer <api_key>'"}
                )
        else:
            # For endpoints that require authentication, return 401 if no auth header
            # For now, we'll require API key for all non-public endpoints
            if request.url.path.startswith("/api/") and not is_public_rag_endpoint:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "API key is required"}
                )

        response = await call_next(request)
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Basic rate limiting check
        # In a real implementation, you'd use Redis or similar to track requests per IP/key
        is_allowed = await APIKeyValidator.check_rate_limit(request)

        if not is_allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )

        response = await call_next(request)
        return response