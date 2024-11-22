import redis.asyncio as redis
from redis import ConnectionPool

from common.src.logging.logger import AppLogger
from common.src.setup import get_settings

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
