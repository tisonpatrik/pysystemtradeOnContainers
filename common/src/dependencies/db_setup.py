from contextlib import asynccontextmanager
from functools import lru_cache

import asyncpg
from fastapi import FastAPI

from common.src.database.db_settings import get_settings
from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()


@lru_cache
@asynccontextmanager
async def setup_async_database(app: FastAPI):
    settings = get_settings()
    try:
        # Create an asyncpg connection pool
        app.state.async_pool = await asyncpg.create_pool(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            min_size=settings.min_connections,
            max_size=settings.max_connections,
            command_timeout=settings.connection_timeout,
            statement_cache_size=settings.statement_cache_size,
            max_queries=settings.max_queries,
            max_inactive_connection_lifetime=settings.max_inactive_connection_lifetime,
        )
        logger.info("Asyncpg connection pool initialized successfully.")
        yield
    except Exception:
        logger.exception("Failed to initialize Asyncpg connection pool")
        raise
    finally:
        await app.state.async_pool.close()  # type: ignore
        logger.info("Asyncpg connection pool closed successfully.")
