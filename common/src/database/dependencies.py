import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from common.src.database.settings import settings as global_settings
from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()

if global_settings.database_url is None:
    raise ValueError("Database URL must be set")

pool: Pool = None  # Initialize the pool variable globally


async def set_timeouts(connection: asyncpg.Connection):
    # Set a statement timeout (in milliseconds)
    await connection.execute("SET statement_timeout TO 30000")
    # Additional connection configuration can be performed here


async def _init_pool():
    global pool
    connection_string = global_settings.database_url.unicode_string()  # type: ignore
    pool = await asyncpg.create_pool(
        dsn=connection_string,
        min_size=10,
        max_size=10,
        max_queries=50000,
        max_inactive_connection_lifetime=300,
        command_timeout=30,  # Statement timeout in seconds
        init=set_timeouts,  # Connection initialization function
    )


async def get_db() -> Connection:
    global pool
    if pool is None:
        await _init_pool()
    async with pool.acquire() as conn:
        logger.debug("Database connection acquired from the pool.")
        yield conn
