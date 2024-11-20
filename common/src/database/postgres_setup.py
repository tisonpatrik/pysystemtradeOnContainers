import asyncio
from contextlib import asynccontextmanager
from functools import lru_cache

import asyncpg
from fastapi import FastAPI

from common.src.database.errors.dependencies_errors import DatabaseInitializationError
from common.src.logging.logger import AppLogger
from common.src.setup import get_settings

logger = AppLogger.get_instance().get_logger()


@lru_cache
@asynccontextmanager
async def setup_async_database(app: FastAPI):
    settings = get_settings()
    await asyncio.sleep(5)
    try:
        # Create an asyncpg connection pool
        app.state.async_pool = await asyncpg.create_pool(
            host=settings.DB_HOST, port=settings.DB_PORT, user=settings.DB_USER, password=settings.DB_PASSWORD, database=settings.DB_NAME
        )
        logger.info("Asyncpg connection pool initialized successfully.")
        yield
    except asyncpg.PostgresError as e:
        logger.exception("Postgres error during Asyncpg connection pool initialization.")
        raise DatabaseInitializationError("Postgres error during database initialization.") from e
    except Exception as e:
        logger.exception("Unexpected error during Asyncpg connection pool initialization.")
        raise DatabaseInitializationError("Unexpected error during database initialization.") from e
    finally:
        await app.state.async_pool.close()  # type: ignore
        logger.info("Asyncpg connection pool closed successfully.")
