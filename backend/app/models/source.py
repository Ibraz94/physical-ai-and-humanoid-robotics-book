from pydantic import BaseModel

class SourceReference(BaseModel):
    """
    Contains information about where content originated (module/chapter/anchor) for citation purposes
    """
    chunk_id: str
    module: str
    chapter: str
    anchor: str
    url: str

    class Config:
        json_schema_extra = {
            "example": {
                "chunk_id": "chunk_abc123",
                "module": "Foundations",
                "chapter": "Introduction to RAG",
                "anchor": "section-1.2",
                "url": "https://book.example.com/chapter-1#section-1.2"
            }
        }