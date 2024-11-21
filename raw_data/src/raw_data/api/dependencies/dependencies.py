from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.clients.carry_client import CarryClient
from common.src.clients.old_dependencies import (
    get_carry_client,
    get_daily_prices_client,
    get_instruments_client,
    get_redis,
)
from common.src.clients.instruments_client import InstrumentsClient
from common.src.clients.prices_client import PricesClient
from common.src.database.old_postgres_setup import setup_async_database
from common.src.http_client.old_rest_client_setup import setup_async_client
from common.src.redis.old_redis_setup import setup_async_redis
from common.src.redis.redis_repository import RedisRepository
from raw_data.api.handlers.absolute_skew_deviation_handler import AbsoluteSkewDeviationHandler
from raw_data.api.handlers.aggregated_returns_for_asset_class_handler import AggregatedReturnsForAssetClassHandler
from raw_data.api.handlers.average_neg_skew_in_asset_class_for_instrument_handler import AverageNegSkewInAssetClassForInstrumentHandler
from raw_data.api.handlers.cumulative_daily_vol_norm_returns_handler import CumulativeDailyVolNormReturnsHandler
from raw_data.api.handlers.current_average_negskew_over_all_assets_handler import (
    CurrentAverageNegSkewOverAllAssetsHandler,
)
from raw_data.api.handlers.current_average_negskew_over_asset_class_handler import CurrentAverageNegSkewOverAssetClassHandler
from raw_data.api.handlers.daily_annualised_roll_handler import DailyAnnualisedRollHandler
from raw_data.api.handlers.daily_percentage_returns_handler import DailyPercentageReturnsHandler
from raw_data.api.handlers.daily_percentage_volatility_handler import DailyPercentageVolatilityHandler
from raw_data.api.handlers.daily_returns_handler import DailyReturnsHandler
from raw_data.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler
from raw_data.api.handlers.daily_vol_normalized_price_for_asset_handler import (
    DailyVolNormalizedPriceForAssetHandler,
)
from raw_data.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler
from raw_data.api.handlers.fx_prices_handler import FxPricesHandler
from raw_data.api.handlers.historic_average_negskew_all_assets_handler import (
    HistoricAverageNegSkewAllAssetsHandler,
)
from raw_data.api.handlers.instrument_currency_vol_handler import InstrumentCurrencyVolHandler
from raw_data.api.handlers.median_carry_for_asset_class_handler import MedianCarryForAssetClassHandler
from raw_data.api.handlers.neg_skew_all_instruments_handler import NegSkewAllInstrumentsHandler
from raw_data.api.handlers.negskew_over_instrument_list_handler import NegSkewOverInstrumentListHandler
from raw_data.api.handlers.normalize_prices_for_asset_class_handler import NormalizedPricesForAssetClassHandler
from raw_data.api.handlers.raw_carry_handler import RawCarryHandler
from raw_data.api.handlers.relative_skew_deviation_handler import RelativeSkewDeviationHandler
from raw_data.api.handlers.skew_handler import SkewHandler
from raw_data.api.handlers.smooth_carry_handler import SmoothCarryHandler
from raw_data.api.handlers.vol_attenuation_handler import VolAttenuationHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_database(app), setup_async_redis(app), setup_async_client(app):
        yield


def get_daily_returns_handler(
    prices_client: PricesClient = Depends(get_daily_prices_client),
    redis_repository: RedisRepository = Depends(get_redis),
) -> DailyReturnsHandler:
    return DailyReturnsHandler(prices_client=prices_client, redis_repository=redis_repository)


def get_daily_returns_vol_handler(
    prices_client: PricesClient = Depends(get_daily_prices_client),
    redis_repository: RedisRepository = Depends(get_redis),
    daily_returns_handler: DailyReturnsHandler = Depends(get_daily_returns_handler),
) -> DailyReturnsVolHandler:
    return DailyReturnsVolHandler(
        prices_client=prices_client, redis_repository=redis_repository, daily_returns_handler=daily_returns_handler
    )


def get_daily_percentage_volatility_handler(
    prices_client: PricesClient = Depends(get_daily_prices_client),
    redis_repository: RedisRepository = Depends(get_redis),
    daily_returns_vol_handler: DailyReturnsVolHandler = Depends(get_daily_returns_vol_handler),
) -> DailyPercentageVolatilityHandler:
    return DailyPercentageVolatilityHandler(
        prices_client=prices_client,
        redis_repository=redis_repository,
        daily_returns_vol_handler=daily_returns_vol_handler,
    )


def get_instrument_vol_handler(
    prices_client: PricesClient = Depends(get_daily_prices_client),
    instruments_client: InstrumentsClient = Depends(get_instruments_client),
    daily_percentage_volatility_handler: DailyPercentageVolatilityHandler = Depends(get_daily_percentage_volatility_handler),
) -> InstrumentCurrencyVolHandler:
    return InstrumentCurrencyVolHandler(
        prices_client=prices_client,
        instruments_client=instruments_client,
        daily_percentage_volatility_handler=daily_percentage_volatility_handler,
    )


def get_daily_vol_norm_returns_handler(
    prices_client: PricesClient = Depends(get_daily_prices_client),
    daily_returns_vol_handler: DailyReturnsVolHandler = Depends(get_daily_returns_vol_handler),
    redis_repository: RedisRepository = Depends(get_redis),
    daily_returns_handler: DailyReturnsHandler = Depends(get_daily_returns_handler),
) -> DailyvolNormalizedReturnsHandler:
    return DailyvolNormalizedReturnsHandler(
        prices_client=prices_client,
        daily_returns_vol_handler=daily_returns_vol_handler,
        redis_repository=redis_repository,
        daily_returns_handler=daily_returns_handler,
    )


def get_aggregated_returns_for_asset_class_handler(
    instrument_repository: InstrumentsClient = Depends(get_instruments_client),
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


def get_fx_prices_handler(
    instruments_client: InstrumentsClient = Depends(get_instruments_client), prices_client: PricesClient = Depends(get_daily_prices_client)
) -> FxPricesHandler:
    return FxPricesHandler(instruments_client=instruments_client, prices_client=prices_client)


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


def get_daily_percentage_returns_handler(
    prices_client: PricesClient = Depends(get_daily_prices_client),
    daily_returns_handler: DailyReturnsHandler = Depends(get_daily_returns_handler),
) -> DailyPercentageReturnsHandler:
    return DailyPercentageReturnsHandler(prices_client=prices_client, daily_returns_handler=daily_returns_handler)


def get_skew_handler(
    daily_percentage_returns_handler: DailyPercentageReturnsHandler = Depends(get_daily_percentage_returns_handler),
    redis_repository: RedisRepository = Depends(get_redis),
) -> SkewHandler:
    return SkewHandler(daily_percentage_returns_handler=daily_percentage_returns_handler, redis_repository=redis_repository)


def get_negskew_over_instrument_list_handler(
    skew_handler: SkewHandler = Depends(get_skew_handler),
) -> NegSkewOverInstrumentListHandler:
    return NegSkewOverInstrumentListHandler(skew_handler=skew_handler)


def get_negskew_all_instruments_handler(
    instruments_client: InstrumentsClient = Depends(get_instruments_client),
    negskew_over_instrument_list_handler: NegSkewOverInstrumentListHandler = Depends(get_negskew_over_instrument_list_handler),
) -> NegSkewAllInstrumentsHandler:
    return NegSkewAllInstrumentsHandler(
        instruments_client=instruments_client, negskew_over_instrument_list_handler=negskew_over_instrument_list_handler
    )


def get_current_average_negskew_over_all_assets_handler(
    negskew_all_instruments_handler: NegSkewAllInstrumentsHandler = Depends(get_negskew_all_instruments_handler),
) -> CurrentAverageNegSkewOverAllAssetsHandler:
    return CurrentAverageNegSkewOverAllAssetsHandler(negskew_all_instruments_handler=negskew_all_instruments_handler)


def get_historic_average_negskew_all_assets_handler(
    current_average_negskew_over_all_assets_handler: CurrentAverageNegSkewOverAllAssetsHandler = Depends(
        get_current_average_negskew_over_all_assets_handler
    ),
) -> HistoricAverageNegSkewAllAssetsHandler:
    return HistoricAverageNegSkewAllAssetsHandler(
        current_average_negskew_over_all_assets_handler=current_average_negskew_over_all_assets_handler
    )


def get_absolute_skew_deviation_handler(
    historic_negskew_value_all_assets_handler: HistoricAverageNegSkewAllAssetsHandler = Depends(
        get_historic_average_negskew_all_assets_handler
    ),
    skew_handler: SkewHandler = Depends(get_skew_handler),
) -> AbsoluteSkewDeviationHandler:
    return AbsoluteSkewDeviationHandler(
        historic_negskew_value_all_assets_handler=historic_negskew_value_all_assets_handler, skew_handler=skew_handler
    )


def get_current_average_negskew_over_asset_class_handler(
    negskew_over_instrument_list_handler: NegSkewOverInstrumentListHandler = Depends(get_negskew_over_instrument_list_handler),
    instruments_client: InstrumentsClient = Depends(get_instruments_client),
) -> CurrentAverageNegSkewOverAssetClassHandler:
    return CurrentAverageNegSkewOverAssetClassHandler(
        instruments_client=instruments_client, negskew_over_instrument_list_handler=negskew_over_instrument_list_handler
    )


def get_average_neg_skew_in_asset_class_for_instrument_handler(
    current_average_negskew_over_asset_class_handler: CurrentAverageNegSkewOverAssetClassHandler = Depends(
        get_current_average_negskew_over_asset_class_handler
    ),
    instruments_client: InstrumentsClient = Depends(get_instruments_client),
) -> AverageNegSkewInAssetClassForInstrumentHandler:
    return AverageNegSkewInAssetClassForInstrumentHandler(
        instruments_client=instruments_client,
        current_average_negskew_over_asset_class_handler=current_average_negskew_over_asset_class_handler,
    )


def get_relative_skew_deviation_handler(
    average_neg_skew_in_asset_class_for_instrument_handler: AverageNegSkewInAssetClassForInstrumentHandler = Depends(
        get_average_neg_skew_in_asset_class_for_instrument_handler
    ),
    skew_handler: SkewHandler = Depends(get_skew_handler),
) -> RelativeSkewDeviationHandler:
    return RelativeSkewDeviationHandler(
        average_neg_skew_in_asset_class_for_instrument_handler=average_neg_skew_in_asset_class_for_instrument_handler,
        skew_handler=skew_handler,
    )


def get_vol_attenuation_handler(
    daily_percentage_volatility_handler: DailyPercentageVolatilityHandler = Depends(get_daily_percentage_volatility_handler),
    redis_repository: RedisRepository = Depends(get_redis),
) -> VolAttenuationHandler:
    return VolAttenuationHandler(
        daily_percentage_volatility_handler=daily_percentage_volatility_handler,
        redis_repository=redis_repository,
    )
