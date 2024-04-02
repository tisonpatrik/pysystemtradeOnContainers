from contextlib import asynccontextmanager
from functools import lru_cache

import asyncpg
from fastapi import FastAPI

from common.src.database.settings import get_settings
from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()


@lru_cache()
@asynccontextmanager
async def get_db(app: FastAPI):
    settings = get_settings()
    try:
        # Create an asyncpg connection pool
        app.async_pool = await asyncpg.create_pool(  # type: ignore
            dsn=settings.database_url.unicode_string(),
            min_size=settings.min_connections,  # Assuming this is added to Settings
            max_size=settings.max_connections,
            command_timeout=settings.connection_timeout,
            max_queries=50000,  # Example customization
            max_inactive_connection_lifetime=300.0,
        )
        logger.info("Asyncpg connection pool initialized successfully.")
        yield  # Provide the pool to the context
    except Exception as e:
        logger.error(f"Failed to initialize Asyncpg connection pool: {e}")
        raise e
    finally:
        await app.async_pool.close()  # type: ignore
        logger.info("Asyncpg connection pool closed successfully.")
