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
        pool = redis.ConnectionPool.from_url("redis://localhost")
        app.state.redis_client = redis.Redis(connection_pool=pool)
        logger.info("Redis connection pool initialized successfully.")
        yield
    except Exception as e:
        logger.error(f"Failed to initialize Redis connection pool: {e}")
        raise e
    finally:
        await app.state.redis_client.aclose()
        await pool.aclose()
        logger.info("Redis connection pool closed successfully.")