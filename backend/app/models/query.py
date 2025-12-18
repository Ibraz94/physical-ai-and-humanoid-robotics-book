from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from .source import SourceReference

class QueryRequest(BaseModel):
    """
    Represents a user query with context information
    """
    query: str
    context: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are the key principles of RAG systems?",
                "context": {
                    "type": "qdrant",
                    "filters": None,
                    "max_chunks": 10
                },
                "session_id": "sess_12345"
            }
        }

class QueryResponse(BaseModel):
    """
    Contains the answer string and array of citations with chunk_id and source information
    """
    answer: str
    citations: List[SourceReference]
    session_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Retrieval-Augmented Generation (RAG) systems combine information retrieval with text generation...",
                "citations": [
                    {
                        "chunk_id": "chunk_abc123",
                        "module": "Foundations",
                        "chapter": "Introduction to RAG",
                        "anchor": "section-1.2",
                        "url": "https://book.example.com/chapter-1#section-1.2"
                    }
                ],
                "session_id": "sess_12345"
            }
        }

class SelectedTextRequest(BaseModel):
    """
    Request model for user-selected text
    """
    text: str
    source_url: str
    session_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "text": "The key principle of RAG is to ground responses in retrieved context.",
                "source_url": "https://book.example.com/chapter-1",
                "session_id": "sess_12345"
            }
        }

class SelectedTextResponse(BaseModel):
    """
    Response model for processed selected text
    """
    status: str  # "success" or "error"
    message: str
    processed_text_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Selected text processed successfully",
                "processed_text_id": "txt_67890"
            }
        }

class IngestionRequest(BaseModel):
    """
    Request model for triggering content ingestion
    """
    sitemap_url: Optional[str] = None
    urls: Optional[List[str]] = []
    force_refresh: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "sitemap_url": "https://book.example.com/sitemap.xml",
                "urls": ["https://book.example.com/chapter-1", "https://book.example.com/chapter-2"],
                "force_refresh": False
            }
        }

class IngestionResponse(BaseModel):
    """
    Response model for ingestion process
    """
    status: str  # "started", "queued", "processing"
    job_id: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "started",
                "job_id": "job_ingest_123",
                "message": "Ingestion process started successfully"
            }
        }