import redis.asyncio as redis
from redis.asyncio import ConnectionPool

from common.src.app_settings import get_settings
from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()


def setup_async_redis() -> ConnectionPool:
    settings = get_settings()
    try:
        pool = redis.ConnectionPool.from_url(settings.REDIS)
        logger.info("Redis connection pool initialized successfully.")
        return pool
    except redis.ConnectionError:
        logger.exception("Failed to initialize Redis connection pool: ")
        raise
