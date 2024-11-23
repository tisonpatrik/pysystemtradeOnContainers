from contextlib import asynccontextmanager
from functools import lru_cache

import redis.asyncio as redis
from fastapi import FastAPI

from common.src.logging.logger import AppLogger
from common.src.setup import get_settings

logger = AppLogger.get_instance().get_logger()


@lru_cache
@asynccontextmanager
async def setup_async_redis(app: FastAPI):
    try:
        # Create a Redis connection pool
        settings = get_settings()
        pool = redis.ConnectionPool.from_url(settings.REDIS)
        app.state.redis_pool = pool
        logger.info("Redis connection pool initialized successfully.")
        yield
    except redis.ConnectionError:
        logger.exception("Failed to initialize Redis connection pool: ")
        raise
    finally:
        await app.state.redis_pool.aclose()  # type: ignore
        logger.info("Redis connection pool closed successfully.")