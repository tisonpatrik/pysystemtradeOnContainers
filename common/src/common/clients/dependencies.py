from grpc.aio import Channel

from common.app_settings import get_settings
from common.clients.instruments_client import InstrumentsClient
from common.clients.prices_client import PricesClient
from common.clients.raw_data_client import RawDataClient
from common.database.postgres_setup import setup_async_database
from common.database.repository import PostgresClient
from common.grpc.grpc_setup import setup_grpc_channel
from common.http_client.rest_client import RestClient
from common.http_client.rest_client_setup import setup_async_client
from common.redis.redis_repository import RedisClient
from common.redis.redis_setup import setup_async_redis


async def get_database_async() -> PostgresClient:
    pool = await setup_async_database()
    return PostgresClient(pool)


async def get_rest_client_async() -> RestClient:
    pool = await setup_async_client()
    return RestClient(pool)


def get_redis() -> RedisClient:
    pool = setup_async_redis()
    return RedisClient(pool)


async def get_raw_data_channel() -> Channel:
    settings = get_settings()
    channel = await setup_grpc_channel(settings.RAW_DATA_SERVICE_ADDRESS)
    return channel


async def get_raw_data_client() -> RawDataClient:
    channel = await get_raw_data_channel()
    redis = get_redis()
    return RawDataClient(grpc_channel=channel, redis=redis)


def get_daily_prices_client(postgres: PostgresClient, redis: RedisClient) -> PricesClient:
    return PricesClient(postgres=postgres, redis=redis)


def get_instruments_client(postgres: PostgresClient) -> InstrumentsClient:
    return InstrumentsClient(repository=postgres)
