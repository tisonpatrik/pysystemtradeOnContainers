from fastapi import Depends, Request

from common.src.database.repository import Repository
from raw_data.src.api.handlers.fx_prices_handler import FxPricesHandler
from raw_data.src.services.adjusted_prices_service import AdjustedPricesService
from raw_data.src.services.instrument_config_service import InstrumentConfigService
from raw_data.src.services.multiple_prices_service import MultiplePricesService


def get_repository(request: Request) -> Repository:
    return Repository(request.app.async_pool)


def get_instrument_config_service(repository: Repository = Depends(get_repository)) -> InstrumentConfigService:
    """
    Dependency injection method for InstrumentConfigService.
    """
    return InstrumentConfigService(repository=repository)


def get_adjusted_prices_service(repository: Repository = Depends(get_repository)) -> AdjustedPricesService:
    """
    Dependency injection method for AdjustedPricesService.
    """
    return AdjustedPricesService(repository=repository)


def get_multiple_prices_service(repository: Repository = Depends(get_repository)) -> MultiplePricesService:
    """
    Dependency injection method for MultiplePricesService.
    """
    return MultiplePricesService(repository=repository)

def get_fx_prices_handler(repository: Repository = Depends(get_repository)) -> FxPricesHandler:
    return FxPricesHandler(repository=repository)