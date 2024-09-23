from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.dependencies.core_dependencies import get_daily_prices_repository, get_instruments_repository, get_redis
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.redis_setup import setup_async_redis
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.repositories.prices_repository import PricesRepository
from risk.src.api.handlers.aggregated_returns_for_asset_class_handler import AggregatedReturnsForAssetClassHandler
from risk.src.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler
from risk.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler
from risk.src.api.handlers.instrument_currency_vol_handler import InstrumentCurrencyVolHandler
from risk.src.api.handlers.normalize_prices_for_asset_class_handler import NormalizedPricesForAssetClassHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_database(app), setup_async_redis(app):
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


def get_daily_vol_normalized_returns_handler(
    prices_repository: PricesRepository = Depends(get_daily_prices_repository),
    daily_returns_vol_handler: DailyReturnsVolHandler = Depends(get_daily_returns_vol_handler),
    redis_repository: RedisRepository = Depends(get_redis),
) -> DailyvolNormalizedReturnsHandler:
    return DailyvolNormalizedReturnsHandler(
        prices_repository=prices_repository, daily_returns_vol_handler=daily_returns_vol_handler, redis_repository=redis_repository
    )


def get_aggregated_returns_for_asset_class_handler(
    instrument_repository: InstrumentsRepository = Depends(get_instruments_repository),
    daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler = Depends(get_daily_vol_normalized_returns_handler),
    redis_repository: RedisRepository = Depends(get_redis),
) -> AggregatedReturnsForAssetClassHandler:
    return AggregatedReturnsForAssetClassHandler(
        instrument_repository=instrument_repository,
        daily_vol_normalized_returns_handler=daily_vol_normalized_returns_handler,
        redis_repository=redis_repository,
    )


def get_normalized_price_for_asset_class_handler(
    daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler = Depends(get_daily_vol_normalized_returns_handler),
    aggregated_returns_handler: AggregatedReturnsForAssetClassHandler = Depends(get_aggregated_returns_for_asset_class_handler),
) -> NormalizedPricesForAssetClassHandler:
    return NormalizedPricesForAssetClassHandler(
        daily_vol_normalized_returns_handler=daily_vol_normalized_returns_handler,
        aggregated_returns_for_asset_class_handler=aggregated_returns_handler,
    )
