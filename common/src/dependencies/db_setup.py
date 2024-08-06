from contextlib import asynccontextmanager
from functools import lru_cache

import asyncpg
from fastapi import FastAPI

from common.src.database.db_settings import get_settings
from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()


@lru_cache()
@asynccontextmanager
async def setup_async_database(app: FastAPI):
    settings = get_settings()
    print(settings)
    try:
        # Create an asyncpg connection pool
        app.state.async_pool = await asyncpg.create_pool(  
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB,
            min_size=settings.min_connections,
            max_size=settings.max_connections,
            command_timeout=settings.connection_timeout,
            max_queries=50000,
            max_inactive_connection_lifetime=300.0,
        )
        logger.info("Asyncpg connection pool initialized successfully.")
        yield  
    except Exception as e:
        logger.error(f"Failed to initialize Asyncpg connection pool: {e}")
        raise e
    finally:
        await app.state.async_pool.close()  # type: ignore
        logger.info("Asyncpg connection pool closed successfully.")
