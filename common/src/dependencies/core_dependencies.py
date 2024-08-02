from fastapi import Depends, Request

from common.src.database.repository import Repository
from common.src.http_client.rest_client import RestClient
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.repositories.prices_repository import PricesRepository
from common.src.repositories.raw_data_client import RawDataClient
from common.src.repositories.risk_client import RiskClient


def get_repository(request: Request) -> Repository:
    return Repository(request.app.async_pool)


def get_client(request: Request) -> RestClient:
    return RestClient(request.app.state.requests_client)


def get_redis(request: Request) -> RedisRepository:
    return RedisRepository(request.app.state.redis_pool)


def get_daily_prices_repository(
    repository: Repository = Depends(get_repository),
) -> PricesRepository:
    return PricesRepository(repository=repository)


def get_instruments_repository(
    repository: Repository = Depends(get_repository),
) -> InstrumentsRepository:
    return InstrumentsRepository(repository=repository)


def get_risk_client(
    client: RestClient = Depends(get_client),
) -> RiskClient:
    return RiskClient(client=client)


def get_raw_data_client(client: RestClient = Depends(get_client)) -> RawDataClient:
    return RawDataClient(client=client)
