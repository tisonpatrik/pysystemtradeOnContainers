from fastapi import Depends

from common.src.clients.account_client import AccountClient
from common.src.clients.carry_client import CarryClient
from common.src.clients.forecast_client import ForecastClient
from common.src.clients.instruments_client import InstrumentsClient
from common.src.clients.prices_client import PricesClient
from common.src.clients.raw_data_client import RawDataClient
from common.src.clients.rules_signals_client import RulesSignalsClient
from common.src.database.postgres_setup import setup_async_database
from common.src.database.repository import PostgresClient
from common.src.http_client.rest_client import RestClient
from common.src.http_client.rest_client_setup import setup_async_client
from common.src.redis.redis_repository import RedisClient
from common.src.redis.redis_setup import setup_async_redis


async def get_database_async() -> PostgresClient:
    pool = await setup_async_database()
    return PostgresClient(pool)


async def get_rest_client_async() -> RestClient:
    pool = await setup_async_client()
    return RestClient(pool)


def get_redis() -> RedisClient:
    pool = setup_async_redis()
    return RedisClient(pool)


def get_account_client(
    rest_client: RestClient = Depends(get_rest_client_async),
) -> AccountClient:
    return AccountClient(rest_client=rest_client)


def get_daily_prices_client(postgres: PostgresClient, redis: RedisClient) -> PricesClient:
    return PricesClient(postgres=postgres, redis=redis)


def get_carry_client(
    db_repository: PostgresClient = Depends(get_database_async),
    redis_repository: RedisClient = Depends(get_redis),
    rest_client: RestClient = Depends(get_rest_client_async),
) -> CarryClient:
    return CarryClient(db_repository=db_repository, redis_repository=redis_repository, rest_client=rest_client)


def get_instruments_client(postgres: PostgresClient) -> InstrumentsClient:
    return InstrumentsClient(repository=postgres)


def get_raw_data_client(
    rest_client: RestClient = Depends(get_rest_client_async),
    redis_repository: RedisClient = Depends(get_redis),
) -> RawDataClient:
    return RawDataClient(rest_client=rest_client, redis_repository=redis_repository)


def get_rules_signals_client(
    db_repository: PostgresClient = Depends(get_database_async),
    rest_client: RestClient = Depends(get_rest_client_async),
) -> RulesSignalsClient:
    return RulesSignalsClient(db_repository=db_repository, rest_client=rest_client)


def get_forecast_client() -> ForecastClient:
    return ForecastClient()
