from common.clients.carry_client import CarryClient
from common.clients.forecast_client import ForecastClient
from common.clients.instruments_client import InstrumentsClient
from common.clients.prices_client import PricesClient
from common.database.postgres_setup import setup_async_database
from common.database.repository import PostgresClient
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


def get_daily_prices_client(postgres: PostgresClient, redis: RedisClient) -> PricesClient:
    return PricesClient(postgres=postgres, redis=redis)


def get_carry_client(postgres: PostgresClient) -> CarryClient:
    return CarryClient(postgres=postgres)


def get_instruments_client(postgres: PostgresClient) -> InstrumentsClient:
    return InstrumentsClient(repository=postgres)


def get_forecast_client() -> ForecastClient:
    return ForecastClient()
