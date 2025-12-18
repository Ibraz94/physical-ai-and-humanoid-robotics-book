"""
Session model for managing user sessions
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Session(BaseModel):
    """
    Represents a user session with metadata and personalization data
    """
    session_id: str
    created_at: datetime
    updated_at: datetime
    user_id: Optional[str] = None
    metadata: Optional[dict] = {}
    personalization_data: Optional[dict] = {}

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "sess_12345",
                "created_at": "2025-12-18T10:00:00Z",
                "updated_at": "2025-12-18T10:05:00Z",
                "user_id": "user_67890",
                "metadata": {"device": "mobile", "location": "US"},
                "personalization_data": {"preferences": {"theme": "dark"}}
            }
        }