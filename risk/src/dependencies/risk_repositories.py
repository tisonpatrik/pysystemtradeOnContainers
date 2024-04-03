from fastapi import Request

from common.src.database.repository import Repository
from risk.src.models.risk_models import DailyReturnsVolModel, DailyVolNormalizedReturnsModel, InstrumentVolModel


def get_daily_returns_vol_repository(request: Request) -> Repository[DailyReturnsVolModel]:
    return Repository(request.app.async_pool, DailyReturnsVolModel)


def get_instrument_vol_repository(request: Request) -> Repository[InstrumentVolModel]:
    return Repository(request.app.async_pool, InstrumentVolModel)


def get_daily_vol_normalised_returns_repository(request: Request) -> Repository[DailyVolNormalizedReturnsModel]:
    return Repository(request.app.async_pool, DailyVolNormalizedReturnsModel)


def get_daily_vol_normalised_price_for_asset_class_repository(
    request: Request,
) -> Repository[DailyVolNormalizedReturnsModel]:
    return Repository(request.app.async_pool, DailyVolNormalizedReturnsModel)
