from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.database.repository import Repository
from common.src.repositories.daily_prices_repository import DailyPricesRepository
from common.src.dependencies.core_dependencies import get_repository, get_daily_prices_repository
from common.src.dependencies.db_setup import setup_async_database
from risk.src.api.handlers.daily_returns_volatility_handler import DailyReturnsVolHandler
from risk.src.api.handlers.instrument_currency_vol_handler import InstrumentCurrencyVolHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_database(app):
        yield


async def get_instrument_vol_handler(repository: Repository = Depends(get_repository)) -> InstrumentCurrencyVolHandler:
    return InstrumentCurrencyVolHandler(repository=repository)


async def get_daily_returns_vol_handler(
    daily_prices_repository: DailyPricesRepository = Depends(get_daily_prices_repository),
) -> DailyReturnsVolHandler:
    return DailyReturnsVolHandler(repository=daily_prices_repository)
