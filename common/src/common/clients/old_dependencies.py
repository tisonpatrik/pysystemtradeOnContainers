from fastapi import Depends, Request

from common.clients.account_client import AccountClient
from common.clients.forecast_client import ForecastClient
from common.clients.instruments_client import InstrumentsClient
from common.clients.old_carry_client import CarryClient
from common.clients.prices_client import PricesClient
from common.clients.raw_data_client import RawDataClient
from common.clients.rules_signals_client import RulesSignalsClient
from common.database.repository import PostgresClient
from common.http_client.rest_client import RestClient
from common.redis.redis_repository import RedisClient


def get_database(request: Request) -> PostgresClient:
    return PostgresClient(request.app.state.async_pool)


def get_rest_client(request: Request) -> RestClient:
    return RestClient(request.app.state.requests_client)


def get_redis(request: Request) -> RedisClient:
    return RedisClient(request.app.state.redis_pool)


def get_account_client(
    rest_client: RestClient = Depends(get_rest_client),
) -> AccountClient:
    return AccountClient(rest_client=rest_client)


def get_daily_prices_client(
    db_repository: PostgresClient = Depends(get_database),
    redis_repository: RedisClient = Depends(get_redis),
) -> PricesClient:
    return PricesClient(postgres=db_repository, redis=redis_repository)


def get_carry_client(
    postgres: PostgresClient = Depends(get_database),
    redis_repository: RedisClient = Depends(get_redis),
    rest_client: RestClient = Depends(get_rest_client),
) -> CarryClient:
    return CarryClient(postgres=postgres, redis=redis_repository, rest_client=rest_client)


def get_instruments_client(
    repository: PostgresClient = Depends(get_database),
) -> InstrumentsClient:
    return InstrumentsClient(repository=repository)


def get_raw_data_client(
    rest_client: RestClient = Depends(get_rest_client),
    redis_repository: RedisClient = Depends(get_redis),
) -> RawDataClient:
    return RawDataClient(rest_client=rest_client, redis_repository=redis_repository)


def get_rules_signals_client(
    db_repository: PostgresClient = Depends(get_database),
    rest_client: RestClient = Depends(get_rest_client),
) -> RulesSignalsClient:
    return RulesSignalsClient(db_repository=db_repository, rest_client=rest_client)


def get_forecast_client() -> ForecastClient:
    return ForecastClient()
