from fastapi import Depends

from common.src.database.repository import Repository
from risk.src.dependencies.risk_repositories import get_daily_returns_vol_repository
from risk.src.models.risk_models import DailyReturnsVolatility
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService


def get_daily_returns_vol_service(
    repository: Repository[DailyReturnsVolatility] = Depends(get_daily_returns_vol_repository),
) -> DailyReturnsVolService:
    """
    Dependency injection method for AdjustedPricesService.
    """
    return DailyReturnsVolService(repository=repository)
