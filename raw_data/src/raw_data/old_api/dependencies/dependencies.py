from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.clients.carry_client import CarryClient
from common.src.clients.instruments_client import InstrumentsClient
from common.src.clients.old_dependencies import (
    get_carry_client,
    get_daily_prices_client,
    get_instruments_client,
    get_redis,
)
from common.src.clients.prices_client import PricesClient
from common.src.database.old_postgres_setup import setup_async_database
from common.src.http_client.old_rest_client_setup import setup_async_client
from common.src.redis.old_redis_setup import setup_async_redis
from common.src.redis.redis_repository import RedisClient
from raw_data.api.handlers.daily_percentage_volatility_handler import DailyPercentageVolatilityHandler
from raw_data.api.handlers.daily_returns_handler import DailyReturnsHandler
from raw_data.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler
from raw_data.old_api.handlers.aggregated_returns_for_asset_class_handler import AggregatedReturnsForAssetClassHandler
from raw_data.old_api.handlers.daily_annualised_roll_handler import DailyAnnualisedRollHandler
from raw_data.old_api.handlers.daily_vol_normalized_price_for_asset_handler import (
    DailyVolNormalizedPriceForAssetHandler,
)
from raw_data.old_api.handlers.median_carry_for_asset_class_handler import MedianCarryForAssetClassHandler
from raw_data.old_api.handlers.normalize_prices_for_asset_class_handler import NormalizedPricesForAssetClassHandler
from raw_data.old_api.handlers.raw_carry_handler import RawCarryHandler
from raw_data.old_api.handlers.smooth_carry_handler import SmoothCarryHandler
from raw_data.src.raw_data.api.handlers.cumulative_daily_vol_norm_returns_handler import CumulativeDailyVolNormReturnsHandler
from raw_data.src.raw_data.api.handlers.daily_vol_normalized_returns_handler import DailyVolNormalizedReturnsHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_database(app), setup_async_redis(app), setup_async_client(app):
        yield


def get_daily_returns_handler(
    prices_client: PricesClient = Depends(get_daily_prices_client),
    redis_repository: RedisClient = Depends(get_redis),
) -> DailyReturnsHandler:
    return DailyReturnsHandler(prices_client=prices_client, redis=redis_repository)


def get_daily_returns_vol_handler(
    prices_client: PricesClient = Depends(get_daily_prices_client),
    redis_repository: RedisClient = Depends(get_redis),
    daily_returns_handler: DailyReturnsHandler = Depends(get_daily_returns_handler),
) -> DailyReturnsVolHandler:
    return DailyReturnsVolHandler(prices_client=prices_client, redis=redis_repository, daily_returns_handler=daily_returns_handler)


def get_daily_percentage_volatility_handler(
    prices_client: PricesClient = Depends(get_daily_prices_client),
    redis_repository: RedisClient = Depends(get_redis),
    daily_returns_vol_handler: DailyReturnsVolHandler = Depends(get_daily_returns_vol_handler),
) -> DailyPercentageVolatilityHandler:
    return DailyPercentageVolatilityHandler(
        prices_client=prices_client,
        redis_repository=redis_repository,
        daily_returns_vol_handler=daily_returns_vol_handler,
    )


def get_daily_vol_norm_returns_handler(
    prices_client: PricesClient = Depends(get_daily_prices_client),
    daily_returns_vol_handler: DailyReturnsVolHandler = Depends(get_daily_returns_vol_handler),
    redis_repository: RedisClient = Depends(get_redis),
    daily_returns_handler: DailyReturnsHandler = Depends(get_daily_returns_handler),
) -> DailyVolNormalizedReturnsHandler:
    return DailyVolNormalizedReturnsHandler(
        prices_client=prices_client,
        daily_returns_vol_handler=daily_returns_vol_handler,
        redis=redis_repository,
        daily_returns_handler=daily_returns_handler,
    )


def get_aggregated_returns_for_asset_class_handler(
    instrument_repository: InstrumentsClient = Depends(get_instruments_client),
    daily_vol_normalized_returns_handler: DailyVolNormalizedReturnsHandler = Depends(get_daily_vol_norm_returns_handler),
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
    get_daily_vol_norm_returns_handler: DailyVolNormalizedReturnsHandler = Depends(get_daily_vol_norm_returns_handler),
    redis_repository: RedisClient = Depends(get_redis),
) -> CumulativeDailyVolNormReturnsHandler:
    return CumulativeDailyVolNormReturnsHandler(
        daily_vol_normalized_returns_handler=get_daily_vol_norm_returns_handler,
        redis=redis_repository,
    )


def get_normalized_price_for_asset_class_handler(
    instruments_client: InstrumentsClient = Depends(get_instruments_client),
    daily_vol_normalized_price_for_asset_handler: DailyVolNormalizedPriceForAssetHandler = Depends(
        get_daily_vol_normalized_price_for_asset_class_handler
    ),
    cumulative_daily_vol_norm_returns_handler: CumulativeDailyVolNormReturnsHandler = Depends(
        get_cumulative_daily_vol_norm_returns_handler
    ),
) -> NormalizedPricesForAssetClassHandler:
    return NormalizedPricesForAssetClassHandler(
        instruments_client=instruments_client,
        daily_vol_normalized_price_for_asset_handler=daily_vol_normalized_price_for_asset_handler,
        cumulative_daily_vol_norm_returns_handler=cumulative_daily_vol_norm_returns_handler,
    )


def get_annualised_roll_handler(carry_client: CarryClient = Depends(get_carry_client)) -> DailyAnnualisedRollHandler:
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


def get_median_carry_for_asset_class_handler(
    raw_carry_handler: RawCarryHandler = Depends(get_raw_carry_handler),
    instrument_repository: InstrumentsClient = Depends(get_instruments_client),
) -> MedianCarryForAssetClassHandler:
    return MedianCarryForAssetClassHandler(raw_carry_handler=raw_carry_handler, instrument_client=instrument_repository)
