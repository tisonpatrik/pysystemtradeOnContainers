import asyncpg
from asyncpg.pool import Pool

from common.src.database.errors.dependencies_errors import DatabaseInitializationError
from common.src.logging.logger import AppLogger
from common.src.setup import get_settings

logger = AppLogger.get_instance().get_logger()


async def setup_async_database() -> Pool:
    """
    Set up an asyncpg connection pool.
    This function manages the lifecycle of the connection pool.
    """
    settings = get_settings()
    try:
        # Create an asyncpg connection pool
        pool = await asyncpg.create_pool(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
        )
        logger.info("Asyncpg connection pool initialized successfully.")
        return pool
    except asyncpg.PostgresError as e:
        logger.exception("Postgres error during Asyncpg connection pool initialization.")
        raise DatabaseInitializationError("Postgres error during database initialization.") from e
    except Exception as e:
        logger.exception("Unexpected error during Asyncpg connection pool initialization.")
        raise DatabaseInitializationError("Unexpected error during database initialization.") from e
