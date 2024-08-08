import json

import redis.asyncio as redis

from common.src.logging.logger import AppLogger
from common.src.redis.base_statements.get_cache_statement import GetCacheStatement
from common.src.redis.base_statements.set_cache_statement import SetCacheStatement


class RedisRepository:
    def __init__(self, pool: redis.ConnectionPool):
        self.redis_client = redis.Redis(connection_pool=pool)
        self.logger = AppLogger.get_instance().get_logger()

    async def get_cache(self, statement: GetCacheStatement) ->  dict | None:

        try:
            value = await self.redis_client.get(statement.cache_key)
            if value is None:
                self.logger.info(f"Cache miss for key '{statement.cache_key}'")
                return None
            return json.loads(value)
        except Exception as e:
            self.logger.error(f"Failed to get cache for key '{statement.cache_key}': {e}")
            raise

    async def set_cache(self, statement: SetCacheStatement) -> None:
        try:
            await self.redis_client.set(statement.cache_key, json.dumps(statement.cache_value), ex=statement.time_to_live)
            self.logger.info(f"Cache set for key '{statement.cache_key}' with TTL {statement.time_to_live}s")
        except Exception as e:
            self.logger.error(f"Failed to set cache for key '{statement.cache_key}': {e}")
            raise

    async def delete_cache(self, key: str) -> None:
        try:
            await self.redis_client.delete(key)
            self.logger.info(f"Cache deleted for key '{key}'")
        except Exception as e:
            self.logger.error(f"Failed to delete cache for key '{key}': {e}")
            raise
