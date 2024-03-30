from fastapi import Request

from common.src.database.repository import Repository
from risk.src.models.risk_models import DailyReturnsVolModel


def get_daily_returns_vol_repository(request: Request) -> Repository[DailyReturnsVolModel]:
    return Repository(request.app.async_pool, DailyReturnsVolModel)
