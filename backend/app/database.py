"""
Database connection setup for Neon Serverless Postgres
"""
import asyncpg
from typing import Optional
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Global database connection pool
_pool: Optional[asyncpg.Pool] = None

async def init_db_pool() -> asyncpg.Pool:
    """
    Initialize the database connection pool
    """
    global _pool

    if _pool is None:
        try:
            _pool = await asyncpg.create_pool(
                dsn=settings.database_url,
                min_size=1,
                max_size=10,
                command_timeout=60,
            )
            logger.info("Database connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database connection pool: {e}")
            raise

    return _pool

async def get_db_connection():
    """
    Get a database connection from the pool
    """
    if _pool is None:
        await init_db_pool()

    return _pool

async def close_db_pool():
    """
    Close the database connection pool
    """
    global _pool
    if _pool:
        _pool.close()
        await _pool.wait_closed()
        _pool = None
        logger.info("Database connection pool closed")