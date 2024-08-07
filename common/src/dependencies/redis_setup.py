from contextlib import asynccontextmanager
from functools import lru_cache

import redis.asyncio as redis
from fastapi import FastAPI

from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()


@lru_cache()
@asynccontextmanager
async def setup_async_redis(app: FastAPI):
    try:
        # Create a Redis connection pool
        pool = redis.ConnectionPool.from_url("redis://redis:6380")
        app.state.redis_pool = pool
        logger.info("Redis connection pool initialized successfully.")
        yield
    except redis.ConnectionError as e:
        logger.error(f"Failed to initialize Redis connection pool: {e}")
        raise e
    finally:
        await app.state.redis_pool.aclose()  # type: ignore
        logger.info("Redis connection pool closed successfully.")
