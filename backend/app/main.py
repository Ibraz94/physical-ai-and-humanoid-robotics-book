from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import os
from dotenv import load_dotenv
from .middleware import SecurityMiddleware, APIKeyValidationMiddleware, RateLimitMiddleware

# Load environment variables
load_dotenv()

app = FastAPI(
    title="RAG Chatbot Backend API",
    description="API for the RAG chatbot backend with OpenAI Agents SDK integration",
    version="1.0.0"
)

# Add security and performance middleware
app.add_middleware(SecurityMiddleware)
app.add_middleware(APIKeyValidationMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)

# Configure CORS - restricted to deployed book domain
book_domain = os.getenv("BOOK_DOMAIN", "*")  # Default to wildcard for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[book_domain],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Add this if you need to allow credentials
    # expose_headers=["Access-Control-Allow-Origin"]
)

# Add trusted host middleware to prevent HTTP Host Header attacks
allowed_hosts = [book_domain, "localhost", "127.0.0.1", "0.0.0.0"]
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=allowed_hosts
)

@app.get("/")
async def root():
    return {"message": "RAG Chatbot Backend API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include API routes
from .api.v1 import query, select, sources, ingest
app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(select.router, prefix="/api/v1", tags=["select"])
app.include_router(sources.router, prefix="/api/v1", tags=["sources"])
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])

# Additional routes will be added as they're implemented

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)