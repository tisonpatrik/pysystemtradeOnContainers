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
from common.src.redis.redis_repository import RedisRepository
from common.src.redis.redis_setup import setup_async_redis


async def get_database_async() -> PostgresClient:
    pool = await setup_async_database()
    return PostgresClient(pool)


async def get_rest_client_async() -> RestClient:
    pool = await setup_async_client()
    return RestClient(pool)


async def get_redis_async() -> RedisRepository:
    pool = await setup_async_redis()
    return RedisRepository(pool)


def get_account_client(
    rest_client: RestClient = Depends(get_rest_client_async),
) -> AccountClient:
    return AccountClient(rest_client=rest_client)


async def get_daily_prices_client_async() -> PricesClient:
    db_repository = await get_database_async()
    redis_repository = await get_redis_async()
    return PricesClient(db_repository=db_repository, redis_repository=redis_repository)


def get_carry_client(
    db_repository: PostgresClient = Depends(get_database_async),
    redis_repository: RedisRepository = Depends(get_redis_async),
    rest_client: RestClient = Depends(get_rest_client_async),
) -> CarryClient:
    return CarryClient(db_repository=db_repository, redis_repository=redis_repository, rest_client=rest_client)


async def get_instruments_client_async() -> InstrumentsClient:
    repository = await get_database_async()
    return InstrumentsClient(repository=repository)


def get_raw_data_client(
    rest_client: RestClient = Depends(get_rest_client_async),
    redis_repository: RedisRepository = Depends(get_redis_async),
) -> RawDataClient:
    return RawDataClient(rest_client=rest_client, redis_repository=redis_repository)


def get_rules_signals_client(
    db_repository: PostgresClient = Depends(get_database_async),
    rest_client: RestClient = Depends(get_rest_client_async),
) -> RulesSignalsClient:
    return RulesSignalsClient(db_repository=db_repository, rest_client=rest_client)


def get_forecast_client() -> ForecastClient:
    return ForecastClient()
