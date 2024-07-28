from fastapi import Depends, Request

from common.src.database.repository import Repository
from common.src.http_client.rest_client import RestClient
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.repositories.prices_repository import PricesRepository


def get_repository(request: Request) -> Repository:
    return Repository(request.app.async_pool)


def get_client(request: Request) -> RestClient:
    return RestClient(request.app.state.requests_client)


def get_daily_prices_repository(
    repository: Repository = Depends(get_repository),
) -> PricesRepository:
    return PricesRepository(repository=repository)


def get_instruments_repository(
    repository: Repository = Depends(get_repository),
) -> InstrumentsRepository:
    return InstrumentsRepository(repository=repository)
