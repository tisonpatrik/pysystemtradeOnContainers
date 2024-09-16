import asyncio
import json

import redis.asyncio as redis

from common.src.logging.logger import AppLogger
from common.src.redis.base_statements.get_cache_statement import GetCacheStatement
from common.src.redis.base_statements.set_cache_statement import SetCacheStatement


class RedisRepository:
    def __init__(self, pool: redis.ConnectionPool):
        self.redis_client = redis.Redis(connection_pool=pool)
        self.logger = AppLogger.get_instance().get_logger()

    async def get_cache(self, statement: GetCacheStatement) -> dict | None:
        try:
            value = await self.redis_client.get(statement.cache_key)
            if value is None:
                self.logger.info("Cache miss for key '%s'", statement.cache_key)
                return None
            self.logger.info("Cache hit for key '%s'", statement.cache_key)
            return json.loads(value)
        except Exception:
            self.logger.exception("Failed to get cache for key '%s'", statement.cache_key)
            raise

    async def set_cache(self, statement: SetCacheStatement) -> None:
        try:
            loop = asyncio.get_event_loop()
            serialized_value = await loop.run_in_executor(None, json.dumps, statement.cache_value)
            await self.redis_client.set(statement.cache_key, serialized_value, ex=statement.time_to_live)
            self.logger.info("Cache set for key '%s' with TTL %ss", statement.cache_key, statement.time_to_live)
        except Exception:
            self.logger.exception("Failed to set cache for key '%s'", statement.cache_key)
            raise
