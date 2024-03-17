from typing import AsyncGenerator

import asyncpg
from asyncpg.pool import Pool

from common.src.database.settings import settings as global_settings
from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()

if global_settings.database_url is None:
    raise ValueError("Database URL must be set")

pool: Pool = None  # Initialize the pool variable globally


async def _init_pool():
    global pool
    connection_string = global_settings.database_url.unicode_string()  # type: ignore
    pool = await asyncpg.create_pool(
        dsn=connection_string,
        min_size=10,
        max_size=10,
        max_queries=50000,
        max_inactive_connection_lifetime=300,
    )


async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    global pool
    if pool is None:
        await _init_pool()
    async with pool.acquire() as conn:  # Use a connection from the pool
        logger.debug("Database connection acquired from the pool.")
        yield conn
