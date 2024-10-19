from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import (
    get_carry_repository,
    get_daily_prices_repository,
    get_db_repository,
    get_instruments_repository,
    get_redis,
)
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.redis_setup import setup_async_redis
from common.src.dependencies.rest_client_setup import setup_async_client
from common.src.redis.redis_repository import RedisRepository
from common.src.repositories.carry_client import CarryClient
from common.src.repositories.instruments_client import InstrumentsClient
from common.src.repositories.prices_client import PricesClient
from raw_data.src.api.handlers.aggregated_returns_for_asset_class_handler import AggregatedReturnsForAssetClassHandler
from raw_data.src.api.handlers.cumulative_daily_vol_norm_returns_handler import CumulativeDailyVolNormReturnsHandler
from raw_data.src.api.handlers.daily_annualised_roll_handler import DailyAnnualisedRollHandler
from raw_data.src.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler
from raw_data.src.api.handlers.daily_vol_normalized_price_for_asset_handler import DailyVolNormalizedPriceForAssetHandler
from raw_data.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler
from raw_data.src.api.handlers.fx_prices_handler import FxPricesHandler
from raw_data.src.api.handlers.instrument_currency_vol_handler import InstrumentCurrencyVolHandler
from raw_data.src.api.handlers.normalize_prices_for_asset_class_handler import NormalizedPricesForAssetClassHandler
from raw_data.src.api.handlers.raw_carry_handler import RawCarryHandler
from raw_data.src.api.handlers.smooth_carry_handler import SmoothCarryHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_database(app), setup_async_redis(app), setup_async_client(app):
        yield


async def get_daily_returns_vol_handler(
    prices_repository: PricesClient = Depends(get_daily_prices_repository),
    redis_repository: RedisRepository = Depends(get_redis),
) -> DailyReturnsVolHandler:
    return DailyReturnsVolHandler(prices_repository=prices_repository, redis_repository=redis_repository)


async def get_instrument_vol_handler(
    prices_repository: PricesClient = Depends(get_daily_prices_repository),
    instruments_repository: InstrumentsClient = Depends(get_instruments_repository),
    daily_returns_vol_handler: DailyReturnsVolHandler = Depends(get_daily_returns_vol_handler),
) -> InstrumentCurrencyVolHandler:
    return InstrumentCurrencyVolHandler(
        prices_repository=prices_repository,
        instruments_repository=instruments_repository,
        daily_returns_vol_handler=daily_returns_vol_handler,
    )


def get_daily_vol_norm_returns_handler(
    prices_repository: PricesClient = Depends(get_daily_prices_repository),
    daily_returns_vol_handler: DailyReturnsVolHandler = Depends(get_daily_returns_vol_handler),
    redis_repository: RedisRepository = Depends(get_redis),
) -> DailyvolNormalizedReturnsHandler:
    return DailyvolNormalizedReturnsHandler(
        prices_repository=prices_repository, daily_returns_vol_handler=daily_returns_vol_handler, redis_repository=redis_repository
    )


def get_aggregated_returns_for_asset_class_handler(
    instrument_repository: InstrumentsClient = Depends(get_instruments_repository),
    daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler = Depends(get_daily_vol_norm_returns_handler),
) -> AggregatedReturnsForAssetClassHandler:
    return AggregatedReturnsForAssetClassHandler(
        instrument_repository=instrument_repository,
        daily_vol_normalized_returns_handler=daily_vol_normalized_returns_handler,
    )


def get_daily_vol_normalized_price_for_asset_class_handler(
    aggregated_returns_handler: AggregatedReturnsForAssetClassHandler = Depends(get_aggregated_returns_for_asset_class_handler),
) -> DailyVolNormalizedPriceForAssetHandler:
    return DailyVolNormalizedPriceForAssetHandler(
        aggregated_returns_for_asset_handler=aggregated_returns_handler,
    )


def get_cumulative_daily_vol_norm_returns_handler(
    get_daily_vol_norm_returns_handler: DailyvolNormalizedReturnsHandler = Depends(get_daily_vol_norm_returns_handler),
    redis_repository: RedisRepository = Depends(get_redis),
) -> CumulativeDailyVolNormReturnsHandler:
    return CumulativeDailyVolNormReturnsHandler(
        daily_vol_normalized_returns_handler=get_daily_vol_norm_returns_handler,
        redis_repository=redis_repository,
    )


def get_normalized_price_for_asset_class_handler(
    daily_vol_normalized_price_for_asset_handler: DailyVolNormalizedPriceForAssetHandler = Depends(
        get_daily_vol_normalized_price_for_asset_class_handler
    ),
    cumulative_daily_vol_norm_returns_handler: CumulativeDailyVolNormReturnsHandler = Depends(
        get_cumulative_daily_vol_norm_returns_handler
    ),
) -> NormalizedPricesForAssetClassHandler:
    return NormalizedPricesForAssetClassHandler(
        daily_vol_normalized_price_for_asset_handler=daily_vol_normalized_price_for_asset_handler,
        cumulative_daily_vol_norm_returns_handler=cumulative_daily_vol_norm_returns_handler,
    )


def get_fx_prices_handler(repository: Repository = Depends(get_db_repository)) -> FxPricesHandler:
    return FxPricesHandler(repository=repository)


def get_annualised_roll_handler(carry_client: CarryClient = Depends(get_carry_repository)) -> DailyAnnualisedRollHandler:
    return DailyAnnualisedRollHandler(carry_client=carry_client)


def get_raw_carry_handler(
    daily_annualised_roll_handler: DailyAnnualisedRollHandler = Depends(get_annualised_roll_handler),
    daily_returns_vol_handler: DailyReturnsVolHandler = Depends(get_daily_returns_vol_handler),
) -> RawCarryHandler:
    return RawCarryHandler(daily_annualised_roll_handler=daily_annualised_roll_handler, daily_returns_vol_handler=daily_returns_vol_handler)


def get_smooth_carry_handler(
    raw_carry_handler: RawCarryHandler = Depends(get_raw_carry_handler),
) -> SmoothCarryHandler:
    return SmoothCarryHandler(raw_carry_handler=raw_carry_handler)
