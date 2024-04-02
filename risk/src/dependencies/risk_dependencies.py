from fastapi import Depends

from common.src.database.repository import Repository
from risk.src.dependencies.risk_repositories import get_daily_returns_vol_repository, get_instrument_vol_repository
from risk.src.models.risk_models import DailyReturnsVolModel, InstrumentVolModel
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService
from risk.src.services.instrument_volatility_service import InstrumentVolService


def get_daily_returns_vol_service(
    repository: Repository[DailyReturnsVolModel] = Depends(get_daily_returns_vol_repository),
) -> DailyReturnsVolService:
    """
    Dependency injection method for DailyReturnsVolService.
    """
    return DailyReturnsVolService(repository=repository)


def get_instrument_vol_service(
    repository: Repository[InstrumentVolModel] = Depends(get_instrument_vol_repository),
) -> InstrumentVolService:
    """
    Dependency injection method for AdjustedPricesService.
    """
    return InstrumentVolService(repository=repository)
