from fastapi import Depends, Request

from common.src.database.repository import Repository
from raw_data.src.models.raw_data_models import (
    AdjustedPricesModel,
    FxPricesModel,
    MultiplePricesModel,
    RollCalendarsModel,
)
from raw_data.src.services.adjusted_prices_service import AdjustedPricesService
from raw_data.src.services.multiple_prices_service import MultiplePricesService


def get_adjusted_prices_repository(request: Request) -> Repository[AdjustedPricesModel]:
    return Repository(request.app.async_pool, AdjustedPricesModel)


def get_fx_prices_repository(request: Request) -> Repository[FxPricesModel]:
    return Repository(request.app.async_pool, FxPricesModel)


def get_multiple_prices_repository(request: Request) -> Repository[MultiplePricesModel]:
    return Repository(request.app.async_pool, MultiplePricesModel)


def get_roll_calendars_repository(request: Request) -> Repository[RollCalendarsModel]:
    return Repository(request.app.async_pool, RollCalendarsModel)


def get_adjusted_prices_service(
    repository: Repository[AdjustedPricesModel] = Depends(get_adjusted_prices_repository),
) -> AdjustedPricesService:
    """
    Dependency injection method for AdjustedPricesService.
    """
    return AdjustedPricesService(repository=repository)


def get_multiple_prices_service(
    repository: Repository[MultiplePricesModel] = Depends(get_multiple_prices_repository),
) -> MultiplePricesService:
    """
    Dependency injection method for MultiplePricesService.
    """
    return MultiplePricesService(repository=repository)
