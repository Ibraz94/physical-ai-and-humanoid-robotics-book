"""
Chunk model for representing content chunks
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Chunk(BaseModel):
    """
    Represents a piece of content from the book with unique ID, text content, and source metadata
    """
    chunk_id: str
    content: str
    source_url: str
    module: str
    chapter: str
    anchor: Optional[str] = ""
    embedding: Optional[List[float]] = []
    created_at: datetime
    metadata: Optional[dict] = {}

    class Config:
        json_schema_extra = {
            "example": {
                "chunk_id": "chunk_abc123",
                "content": "This is a sample content chunk from the book...",
                "source_url": "https://book.example.com/chapter-1",
                "module": "Foundations",
                "chapter": "Introduction",
                "anchor": "section-1.1",
                "embedding": [0.1, 0.2, 0.3],  # Simplified
                "created_at": "2025-12-18T10:00:00Z",
                "metadata": {"token_count": 150, "hash": "abc123"}
            }
        }