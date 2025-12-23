---
sdk: docker
app_port: 7860
---

# RAG Chatbot Backend

This is the backend for the RAG (Retrieval-Augmented Generation) chatbot, designed to work with the OpenAI Agents SDK and Gemini as the reasoning engine.

## Architecture

The backend is built with FastAPI and consists of the following main components:

- **API Layer**: FastAPI endpoints for query processing, content ingestion, and source retrieval
- **Agent Service**: Core logic for processing queries using the OpenAI Agents SDK with Gemini
- **Ingestion Service**: Handles content ingestion from sitemaps and URLs
- **Vector Storage**: Qdrant integration for vector similarity search
- **Embedding Service**: Cohere integration for generating embeddings
- **Persistence Layer**: Neon Serverless Postgres for metadata and session management

## Endpoints

### Query Processing
- `POST /api/v1/query`: Submit a query to the RAG system
- `POST /api/v1/select`: Submit user-selected text for the RAG system
- `GET /api/v1/sources/{chunk_id}`: Get source information for a content chunk
- `POST /api/v1/ingest`: Trigger content ingestion into the knowledge base

## Configuration

The backend requires the following environment variables:

- `DATABASE_URL`: Connection string for Neon Serverless Postgres
- `QDRANT_URL`: URL for Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant (if required)
- `COHERE_API_KEY`: API key for Cohere embeddings
- `GEMINI_API_KEY`: API key for Google Gemini
- `GEMINI_MODEL`: Gemini model to use (default: gemini-pro)
- `BOOK_DOMAIN`: Domain to restrict CORS access to

## Running Locally

```bash
# Install dependencies
uv sync

# Run the development server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Grounding Rules

The system strictly enforces grounding rules:
- Only uses Qdrant-retrieved chunks OR user-selected text
- No external knowledge, browsing, or hallucinations
- Responds with "I don't know based on the provided text." when context is insufficient