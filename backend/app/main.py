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

# Configure CORS - allow communication between frontend and backend
# Include both the book domain and localhost for development
book_domain = os.getenv("BOOK_DOMAIN", "http://localhost:3000")  # Default to frontend dev server
better_auth_url = os.getenv("BETTER_AUTH_URL", "http://localhost:8000")

# Allow origins for both frontend and Better Auth service
allowed_origins = [book_domain, better_auth_url, "http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000", "http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization headers for auth token handling
    expose_headers=["Access-Control-Allow-Origin", "Authorization", "Set-Cookie"]
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
from .api.v1 import query, select, sources, ingest, profile
from .api.auth_handler import get_auth_router, initialize_auth_handler, cleanup_auth_handler
from .database import init_db_pool, close_db_pool

app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(select.router, prefix="/api/v1", tags=["select"])
app.include_router(sources.router, prefix="/api/v1", tags=["sources"])
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])
app.include_router(profile.router, prefix="/api/v1", tags=["profile"])

# Include Better Auth routes (these will be forwarded to the Better Auth service)
auth_router = get_auth_router()
app.include_router(auth_router)

# Additional routes will be added as they're implemented

# Add startup and shutdown events for database and auth handler
@app.on_event("startup")
async def startup_event():
    await init_db_pool()
    await initialize_auth_handler()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db_pool()
    await cleanup_auth_handler()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)