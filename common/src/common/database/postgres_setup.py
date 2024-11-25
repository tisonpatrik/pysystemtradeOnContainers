import asyncio

import asyncpg
from asyncpg import Pool
from asyncpg.exceptions import CannotConnectNowError

from common.app_settings import get_settings
from common.database.errors.dependencies_errors import DatabaseInitializationError
from common.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()


async def setup_async_database(retries: int = 5, delay: int = 2) -> Pool:
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
            if not isinstance(pool, Pool):
                raise DatabaseInitializationError("The created pool is not an instance of asyncpg.Pool.")

            logger.info("Asyncpg connection pool initialized successfully.")
            return pool
        except CannotConnectNowError:
            logger.warning("Database connection failed (attempt %d/%d). Retrying in %ds...", attempt + 1, retries, delay)
            await asyncio.sleep(delay)
        except asyncpg.PostgresError as e:
            logger.exception("Postgres error during Asyncpg connection pool initialization.")
            raise DatabaseInitializationError("Postgres error during database initialization.") from e
    raise DatabaseInitializationError("Unable to connect to database after retries.")
