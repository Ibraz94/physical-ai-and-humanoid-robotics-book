"""
Security utilities and API key validation
"""
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import logging

logger = logging.getLogger(__name__)

# Get API key from environment variable
API_KEY = os.getenv("API_KEY", "dev-api-key-change-in-production")
SECURITY_ENABLED = os.getenv("SECURITY_ENABLED", "false").lower() == "true"

security = HTTPBearer(auto_error=False)  # Don't auto-error, we'll handle manually

class APIKeyValidator:
    @staticmethod
    async def validate_api_key(credentials: HTTPAuthorizationCredentials = None):
        """
        Validate the API key from the Authorization header
        """
        if not SECURITY_ENABLED:
            # If security is disabled, always return True for development
            return True

        if not credentials or not credentials.credentials:
            logger.warning("API key missing from request")
            raise HTTPException(status_code=401, detail="API key is required")

        if credentials.credentials != API_KEY:
            logger.warning("Invalid API key provided")
            raise HTTPException(status_code=401, detail="Invalid API key")

        logger.info("API key validated successfully")
        return True

    @staticmethod
    async def check_rate_limit(request: Request) -> bool:
        """
        Check rate limiting for the request (basic implementation)
        This is a simplified version - in production, you'd use Redis or similar
        """
        # For now, just return True to allow all requests
        # In a real implementation, you would track requests per IP/key and enforce limits
        return True

    @staticmethod
    async def validate_request_origin(request: Request) -> bool:
        """
        Validate that the request is coming from an allowed origin
        """
        # Get the referer header to check the origin
        referer = request.headers.get("referer", "")

        # In production, you'd check against allowed origins
        # For now, we'll allow all origins for development
        return True

    @staticmethod
    async def sanitize_input(input_data: str) -> str:
        """
        Sanitize input to prevent injection attacks
        """
        if not input_data:
            return input_data

        # Remove potentially dangerous characters/sequences
        sanitized = input_data.replace('\0', '').strip()  # Remove null bytes

        # Additional sanitization could be added here
        # For example, remove script tags, etc.

        return sanitized