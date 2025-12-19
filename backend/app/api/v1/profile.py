"""
API endpoints for user profile management.
Handles user profile creation and updates with consent validation.
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from pydantic.functional_validators import field_validator
from typing import Optional
import asyncpg
import os
import uuid
from datetime import datetime
from ...auth import get_current_user, is_endpoint_accessible
from ...database import get_db_connection

router = APIRouter(prefix="/profile", tags=["profile"])

import html
import re

class UserProfileRequest(BaseModel):
    software_background: Optional[str] = Field(
        None,
        description="User's software background information",
        max_length=1000  # Limit length to prevent oversized data
    )
    hardware_background: Optional[str] = Field(
        None,
        description="User's hardware background information",
        max_length=1000  # Limit length to prevent oversized data
    )
    consent_given: bool = Field(..., description="Whether explicit consent was given for data storage")

    @field_validator('software_background', 'hardware_background', mode='before')
    @classmethod
    def sanitize_input(cls, v):
        if v is None:
            return v
        # Sanitize input by removing potentially harmful HTML/JS
        # This is a basic sanitization - in production, consider using a dedicated library
        if isinstance(v, str):
            # Remove HTML tags and escape potentially harmful characters
            v = html.escape(v)
            # Remove script tags (case insensitive)
            v = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', v, flags=re.IGNORECASE)
            # Remove javascript: and data: URIs
            v = re.sub(r'javascript:', '', v, flags=re.IGNORECASE)
            v = re.sub(r'data:', '', v, flags=re.IGNORECASE)
            # Remove potentially harmful content
            v = v.strip()  # Remove leading/trailing whitespace
        return v


class UserProfileResponse(BaseModel):
    id: str
    user_id: str
    software_background: Optional[str]
    hardware_background: Optional[str]
    consent_given: bool
    created_at: datetime
    updated_at: datetime


@router.post("/", response_model=UserProfileResponse)
async def create_or_update_user_profile(
    request: Request,
    profile_data: UserProfileRequest
):
    """
    Create or update user profile with background information.
    Only accessible to authenticated users.
    """
    # Check if endpoint is accessible (user must be authenticated)
    if not await is_endpoint_accessible(request, "/api/v1/profile"):
        raise HTTPException(status_code=401, detail="Authentication required")

    # Get current user from session
    current_user = await get_current_user(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    user_id = current_user.get('user', {}).get('id')
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid session")

    # Validate consent - if consent is not given and background info is provided, reject
    if not profile_data.consent_given and (profile_data.software_background or profile_data.hardware_background):
        raise HTTPException(
            status_code=400,
            detail="Consent must be given to store background information"
        )

    # Generate profile ID if creating new profile
    profile_id = str(uuid.uuid4())

    # Get database pool and acquire a connection
    try:
        pool = await get_db_connection()
        conn = await pool.acquire()
    except Exception as e:
        # Handle database connection failures gracefully
        raise HTTPException(
            status_code=503,
            detail=f"Database service temporarily unavailable: {str(e)}"
        )

    try:
        # Check if profile already exists
        existing_profile_query = """
            SELECT id FROM user_profiles WHERE user_id = $1
        """
        existing_profile = await conn.fetchrow(existing_profile_query, user_id)

        if existing_profile:
            # Update existing profile
            update_query = """
                UPDATE user_profiles
                SET software_background = $1, hardware_background = $2,
                    consent_given = $3, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = $4
                RETURNING *
            """
            result = await conn.fetchrow(
                update_query,
                profile_data.software_background,
                profile_data.hardware_background,
                profile_data.consent_given,
                user_id
            )
        else:
            # Create new profile
            insert_query = """
                INSERT INTO user_profiles (
                    id, user_id, software_background, hardware_background,
                    consent_given, created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING *
            """
            result = await conn.fetchrow(
                insert_query,
                profile_id,
                user_id,
                profile_data.software_background,
                profile_data.hardware_background,
                profile_data.consent_given
            )

        if not result:
            raise HTTPException(status_code=500, detail="Failed to create or update profile")

        return UserProfileResponse(
            id=result['id'],
            user_id=result['user_id'],
            software_background=result['software_background'],
            hardware_background=result['hardware_background'],
            consent_given=result['consent_given'],
            created_at=result['created_at'],
            updated_at=result['updated_at']
        )

    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=409, detail="Profile already exists for this user")
    except asyncpg.PostgreSQLError as e:
        # Handle specific PostgreSQL errors
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        # Handle other database-related errors
        raise HTTPException(status_code=500, detail=f"Unexpected database error: {str(e)}")
    finally:
        await pool.release(conn)


@router.get("/", response_model=UserProfileResponse)
async def get_user_profile(request: Request):
    """
    Get current user's profile information.
    Only accessible to authenticated users.
    """
    # Check if endpoint is accessible (user must be authenticated)
    if not await is_endpoint_accessible(request, "/api/v1/profile"):
        raise HTTPException(status_code=401, detail="Authentication required")

    # Get current user from session
    current_user = await get_current_user(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    user_id = current_user.get('user', {}).get('id')
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid session")

    # Get database pool and acquire a connection
    try:
        pool = await get_db_connection()
        conn = await pool.acquire()
    except Exception as e:
        # Handle database connection failures gracefully
        raise HTTPException(
            status_code=503,
            detail=f"Database service temporarily unavailable: {str(e)}"
        )

    try:
        # Fetch user profile
        query = """
            SELECT * FROM user_profiles WHERE user_id = $1
        """
        result = await conn.fetchrow(query, user_id)

        if not result:
            raise HTTPException(status_code=404, detail="User profile not found")

        return UserProfileResponse(
            id=result['id'],
            user_id=result['user_id'],
            software_background=result['software_background'],
            hardware_background=result['hardware_background'],
            consent_given=result['consent_given'],
            created_at=result['created_at'],
            updated_at=result['updated_at']
        )

    except asyncpg.PostgreSQLError as e:
        # Handle specific PostgreSQL errors
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        # Handle other database-related errors
        raise HTTPException(status_code=500, detail=f"Unexpected database error: {str(e)}")
    finally:
        await pool.release(conn)