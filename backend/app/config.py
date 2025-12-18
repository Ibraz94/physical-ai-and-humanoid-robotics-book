from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv
from pydantic import ConfigDict

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database settings (Neon Serverless Postgres)
    database_url: str = os.getenv("DATABASE_URL", "")

    # Qdrant settings
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")

    # Cohere settings
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")

    # Gemini settings
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-pro")

    # Backend API settings
    backend_api_url: str = os.getenv("BACKEND_API_URL", "http://localhost:8000")

    # Book domain for CORS
    book_domain: str = os.getenv("BOOK_DOMAIN", "http://localhost:3000")

    # Session settings
    session_secret_key: str = os.getenv("SESSION_SECRET_KEY", "dev-secret-key-change-in-production")
    session_algorithm: str = os.getenv("SESSION_ALGORITHM", "HS256")

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # This will ignore extra environment variables
    )

# Create a global settings instance
settings = Settings()