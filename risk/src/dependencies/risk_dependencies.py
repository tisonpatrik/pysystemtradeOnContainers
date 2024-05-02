from fastapi import Depends, Request
from httpx import AsyncClient

from common.src.database.repository import Repository
from risk.src.api.handlers.instrument_volatility_handler import InstrumentVolHandler
from risk.src.api.handlers.test_handler import TestHandler
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService
from risk.src.services.daily_vol_normalised_price_for_asset_class_service import (
    DailyVolNormalisedPriceForAssetClassService,
)
from risk.src.services.daily_vol_normalised_returns_service import DailyVolatilityNormalisedReturnsService
from risk.src.services.instrument_currency_vol_service import InstrumentCurrencyVolService


def get_async_client(request: Request) -> AsyncClient:
    return request.app.state.requests_client


def get_test_handler(
    requests_client: AsyncClient = Depends(get_async_client),
) -> TestHandler:
    return TestHandler(requests_client=requests_client)


def get_repository(request: Request) -> Repository:
    return Repository(request.app.async_pool)


def get_daily_returns_vol_service(
    repository: Repository = Depends(get_repository),
) -> DailyReturnsVolService:
    """
    Dependency injection method for DailyReturnsVolService.
    """
    return DailyReturnsVolService(repository=repository)


def get_instrument_vol_service(
    repository: Repository = Depends(get_repository),
) -> InstrumentCurrencyVolService:
    """
    Dependency injection method for AdjustedPricesService.
    """
    return InstrumentCurrencyVolService(repository=repository)


def get_daily_vol_normalised_returns_service(
    repository: Repository = Depends(get_repository),
) -> DailyVolatilityNormalisedReturnsService:
    """
    Dependency injection method for DailyVolatilityNormalisedReturnsService.
    """
    return DailyVolatilityNormalisedReturnsService(repository=repository)


def get_daily_vol_normalised_price_for_asset_class_service(
    repository: Repository = Depends(get_repository),
) -> DailyVolNormalisedPriceForAssetClassService:
    """
    Dependency injection method for DailyVolNormalisedPriceForAssetClassService.
    """
    return DailyVolNormalisedPriceForAssetClassService(repository=repository)


async def get_instrument_vol_handler(repository: Repository = Depends(get_repository)) -> InstrumentVolHandler:
    return InstrumentVolHandler(repository=repository)
