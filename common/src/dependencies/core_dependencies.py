from fastapi import Depends, Request

from common.src.clients.carry_client import CarryClient
from common.src.clients.forecast_client import ForecastClient
from common.src.clients.instruments_client import InstrumentsClient
from common.src.clients.prices_client import PricesClient
from common.src.clients.raw_data_client import RawDataClient
from common.src.clients.rules_signals_client import RulesSignalsClient
from common.src.database.repository import Repository
from common.src.http_client.rest_client import RestClient
from common.src.redis.redis_repository import RedisRepository


def get_db_repository(request: Request) -> Repository:
    return Repository(request.app.state.async_pool)


def get_client(request: Request) -> RestClient:
    return RestClient(request.app.state.requests_client)


def get_redis(request: Request) -> RedisRepository:
    return RedisRepository(request.app.state.redis_pool)


def get_daily_prices_client(
    db_repository: Repository = Depends(get_db_repository),
    redis_repository: RedisRepository = Depends(get_redis),
) -> PricesClient:
    return PricesClient(db_repository=db_repository, redis_repository=redis_repository)


def get_carry_client(
    db_repository: Repository = Depends(get_db_repository),
    redis_repository: RedisRepository = Depends(get_redis),
    rest_client: RestClient = Depends(get_client),
) -> CarryClient:
    return CarryClient(db_repository=db_repository, redis_repository=redis_repository, rest_client=rest_client)


def get_instruments_client(
    repository: Repository = Depends(get_db_repository),
) -> InstrumentsClient:
    return InstrumentsClient(repository=repository)


def get_raw_data_client(
    rest_client: RestClient = Depends(get_client),
    redis_repository: RedisRepository = Depends(get_redis),
) -> RawDataClient:
    return RawDataClient(rest_client=rest_client, redis_repository=redis_repository)


def get_rules_signals_client(
    db_repository: Repository = Depends(get_db_repository),
) -> RulesSignalsClient:
    return RulesSignalsClient(db_repository=db_repository)


def get_forecast_client() -> ForecastClient:
    return ForecastClient()
