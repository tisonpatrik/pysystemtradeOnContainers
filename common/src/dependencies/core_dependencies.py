from fastapi import Depends, Request

from common.src.database.repository import Repository
from common.src.http_client.rest_client import RestClient
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.repositories.prices_repository import PricesRepository
from common.src.repositories.raw_data_client import RawDataClient
from common.src.repositories.risk_client import RiskClient


def get_db_repository(request: Request) -> Repository:
    return Repository(request.app.state.async_pool)


def get_client(request: Request) -> RestClient:
    return RestClient(request.app.state.requests_client)


def get_redis(request: Request) -> RedisRepository:
    return RedisRepository(request.app.state.redis_pool)


def get_daily_prices_repository(
    db_repository: Repository = Depends(get_db_repository),
    redis_repository: RedisRepository = Depends(get_redis),
) -> PricesRepository:
    return PricesRepository(db_repository=db_repository, redis_repository=redis_repository)


def get_instruments_repository(
    repository: Repository = Depends(get_db_repository),
) -> InstrumentsRepository:
    return InstrumentsRepository(repository=repository)


def get_risk_client(
    rest_client: RestClient = Depends(get_client),
    redis_repository: RedisRepository = Depends(get_redis),
) -> RiskClient:
    return RiskClient(rest_client=rest_client, redis_repository=redis_repository)


def get_raw_data_client(
    rest_client: RestClient = Depends(get_client),
    redis_repository: RedisRepository = Depends(get_redis),
) -> RawDataClient:
    return RawDataClient(rest_client=rest_client, redis_repository=redis_repository)
