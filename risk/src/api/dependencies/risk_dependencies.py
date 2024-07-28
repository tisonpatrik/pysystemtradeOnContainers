from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.dependencies.core_dependencies import get_daily_prices_repository, get_instruments_repository
from common.src.dependencies.db_setup import setup_async_database
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.repositories.prices_repository import PricesRepository
from risk.src.api.handlers.daily_returns_volatility_handler import DailyReturnsVolHandler
from risk.src.api.handlers.instrument_currency_vol_handler import InstrumentCurrencyVolHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_database(app):
        yield


async def get_instrument_vol_handler(
    dprices_repository: PricesRepository = Depends(get_daily_prices_repository),
    instruments_repository: InstrumentsRepository = Depends(get_instruments_repository),
) -> InstrumentCurrencyVolHandler:
    return InstrumentCurrencyVolHandler(prices_repository=dprices_repository, instruments_repository=instruments_repository)


async def get_daily_returns_vol_handler(
    prices_repository: PricesRepository = Depends(get_daily_prices_repository),
) -> DailyReturnsVolHandler:
    return DailyReturnsVolHandler(prices_repository=prices_repository)
