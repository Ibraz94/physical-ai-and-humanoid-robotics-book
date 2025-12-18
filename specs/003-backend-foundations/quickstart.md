# Quickstart Guide: Backend Foundations & OpenAI Agents SDK

## Prerequisites

- Python 3.11+
- uv package manager
- Access to Gemini API
- Access to Cohere API
- Qdrant Cloud account (Free Tier)
- Neon Serverless Postgres account

## Setup

### 1. Clone and Initialize

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Initialize the project with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
uv pip install fastapi openai uvicorn cohere qdrant-client psycopg2-binary
```

### 3. Environment Configuration

Create a `.env` file with the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=your_neon_database_url
CORS_ORIGINS=your_book_domain.com
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── query.py     # /query endpoint
│   │   │   ├── select.py    # /select endpoint
│   │   │   ├── sources.py   # /sources endpoint
│   │   │   └── ingest.py    # /ingest endpoint
│   ├── models/
│   │   ├── __init__.py
│   │   ├── query.py         # QueryRequest, QueryResponse models
│   │   ├── chunk.py         # Chunk model
│   │   └── source.py        # SourceReference model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent_service.py # OpenAI Agents SDK integration
│   │   ├── qdrant_service.py # Vector database operations
│   │   ├── postgres_service.py # Metadata storage operations
│   │   └── ingestion_service.py # Content ingestion logic
│   └── tools/
│       ├── __init__.py
│       └── retrieval_tool.py # Agent tools for RAG
├── tools/
│   └── data_processing/
│       ├── chunker.py       # Content chunking logic
│       └── embedding.py     # Embedding generation
├── ingestion/
│   ├── __init__.py
│   ├── sitemap_parser.py    # Sitemap parsing logic
│   └── content_extractor.py # Content extraction from URLs
└── tests/
    ├── __init__.py
    ├── test_api.py          # API endpoint tests
    ├── test_agent.py        # Agent functionality tests
    └── test_ingestion.py    # Ingestion pipeline tests
```

## Running the Application

### Development

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the FastAPI application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
# Use a production ASGI server like gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## API Endpoints

### POST /query
Submit a query to the RAG system:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key principles of RAG systems?",
    "session_id": "sess_12345"
  }'
```

### POST /select
Submit user-selected text:
```bash
curl -X POST http://localhost:8000/select \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The key principle of RAG is to ground responses in retrieved context.",
    "source_url": "https://book.example.com/chapter-1"
  }'
```

### GET /sources/{chunk_id}
Get source information for a chunk:
```bash
curl http://localhost:8000/sources/chunk_abc123
```

### POST /ingest
Trigger content ingestion:
```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "sitemap_url": "https://book.example.com/sitemap.xml"
  }'
```

## Configuration

### Agent Configuration
The OpenAI Agents SDK will be configured to:
- Use Gemini as the LLM provider
- Enforce strict grounding rules
- Include citations in responses
- Handle insufficient context appropriately

### Database Configuration
- Neon Serverless Postgres for metadata, sessions, and personalization
- Qdrant Cloud for vector storage
- Proper connection pooling and error handling

### CORS Configuration
- Restricted to deployed book domain only
- Proper security headers