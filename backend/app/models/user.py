"""
User model for managing user accounts and consent
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    """
    Represents a user with consent management for data storage
    """
    user_id: str
    email: str
    consent: bool  # Whether user has consented to data storage
    created_at: datetime
    updated_at: Optional[datetime] = None
    preferences: Optional[dict] = {}
    consent_details: Optional[dict] = {}

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_67890",
                "email": "user@example.com",
                "consent": True,
                "created_at": "2025-12-18T10:00:00Z",
                "updated_at": "2025-12-18T10:05:00Z",
                "preferences": {"theme": "dark", "language": "en"},
                "consent_details": {
                    "data_storage": True,
                    "analytics": False,
                    "marketing": False,
                    "consent_date": "2025-12-18T10:00:00Z"
                }
            }
        }