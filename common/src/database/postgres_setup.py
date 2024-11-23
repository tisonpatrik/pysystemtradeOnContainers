import asyncio

import asyncpg
from asyncpg.exceptions import CannotConnectNowError
from asyncpg.pool import Pool

from common.src.database.errors.dependencies_errors import DatabaseInitializationError
from common.src.logging.logger import AppLogger
from common.src.app_settings import get_settings

logger = AppLogger.get_instance().get_logger()


async def setup_async_database(retries=5, delay=2) -> Pool:
    settings = get_settings()
    for attempt in range(retries):
        try:
            pool = await asyncpg.create_pool(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME,
            )
            logger.info("Asyncpg connection pool initialized successfully.")
            return pool
        except CannotConnectNowError:
            logger.warning("Database connection failed (attempt %d/%d). Retrying in %ds...", attempt + 1, retries, delay)
            await asyncio.sleep(delay)
        except asyncpg.PostgresError as e:
            logger.exception("Postgres error during Asyncpg connection pool initialization.")
            raise DatabaseInitializationError("Postgres error during database initialization.") from e
    raise DatabaseInitializationError("Unable to connect to database after retries.")
