from fastapi import Depends

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_repository
from risk.src.api.handlers.instrument_currency_vol_handler import InstrumentCurrencyVolHandler
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService
from risk.src.services.daily_vol_normalised_price_for_asset_class_service import (
    DailyVolNormalisedPriceForAssetClassService,
)
from risk.src.services.daily_vol_normalised_returns_service import DailyVolatilityNormalisedReturnsService
from risk.src.services.instrument_currency_vol_service import InstrumentCurrencyVolService


def get_daily_returns_vol_service() -> DailyReturnsVolService:
    """
    Dependency injection method for DailyReturnsVolService.
    """
    return DailyReturnsVolService()


def get_instrument_vol_service() -> InstrumentCurrencyVolService:
    """
    Dependency injection method for AdjustedPricesService.
    """
    return InstrumentCurrencyVolService()


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


async def get_instrument_vol_handler(repository: Repository = Depends(get_repository)) -> InstrumentCurrencyVolHandler:
    return InstrumentCurrencyVolHandler(repository=repository)
