from fastapi import Depends, Request

from common.src.database.repository import Repository
from common.src.dependencies.database_dependencies import get_db
from raw_data.src.models.raw_data_models import (
    AdjustedPricesModel,
    FxPricesModel,
    MultiplePricesModel,
    RollCalendarsModel,
)
from raw_data.src.services.adjusted_prices_service import AdjustedPricesService


def get_adjusted_prices_repository(request: Request = Depends(get_db)) -> Repository[AdjustedPricesModel]:
    return Repository(request, AdjustedPricesModel)


def get_fx_prices_repository(request: Request = Depends(get_db)) -> Repository[FxPricesModel]:
    return Repository(request, FxPricesModel)


def get_multiple_prices_repository(request: Request = Depends(get_db)) -> Repository[MultiplePricesModel]:
    return Repository(request, MultiplePricesModel)


def get_roll_calendars_repository(request: Request = Depends(get_db)) -> Repository[RollCalendarsModel]:
    return Repository(request, RollCalendarsModel)


def get_adjusted_prices_service(
    repository: Repository[AdjustedPricesModel] = Depends(get_adjusted_prices_repository),
) -> AdjustedPricesService:
    """
    Dependency injection method for AdjustedPricesService.
    """
    return AdjustedPricesService(repository=repository)
