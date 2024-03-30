from fastapi import Depends, Request

from common.src.database.repository import Repository
from common.src.dependencies.database_dependencies import get_db
from risk.src.models.risk_models import DailyReturnsVolModel


def get_daily_returns_vol_repository(request: Request = Depends(get_db)) -> Repository[DailyReturnsVolModel]:
    return Repository(request.app.async_pool, DailyReturnsVolModel)
