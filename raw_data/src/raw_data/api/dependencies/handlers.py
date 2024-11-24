from common.src.clients.dependencies import (
    get_daily_prices_client,
    get_instruments_client,
)
from common.src.database.repository import PostgresClient
from common.src.redis.redis_repository import RedisClient
from raw_data.api.handlers.absolute_skew_deviation_handler import AbsoluteSkewDeviationHandler
from raw_data.api.handlers.average_neg_skew_in_asset_class_for_instrument_handler import (
    AverageNegSkewInAssetClassForInstrumentHandler,
)
from raw_data.api.handlers.current_average_negskew_over_all_assets_handler import (
    CurrentAverageNegSkewOverAllAssetsHandler,
)
from raw_data.api.handlers.current_average_negskew_over_asset_class_handler import CurrentAverageNegSkewOverAssetClassHandler
from raw_data.api.handlers.daily_percentage_returns_handler import DailyPercentageReturnsHandler
from raw_data.api.handlers.daily_percentage_volatility_handler import DailyPercentageVolatilityHandler
from raw_data.api.handlers.daily_returns_handler import DailyReturnsHandler
from raw_data.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler
from raw_data.api.handlers.fx_prices_handler import FxPricesHandler
from raw_data.api.handlers.historic_average_negskew_all_assets_handler import (
    HistoricAverageNegSkewAllAssetsHandler,
)
from raw_data.api.handlers.instrument_currency_vol_handler import InstrumentCurrencyVolHandler
from raw_data.api.handlers.neg_skew_all_instruments_handler import NegSkewAllInstrumentsHandler
from raw_data.api.handlers.negskew_over_instrument_list_handler import NegSkewOverInstrumentListHandler
from raw_data.api.handlers.relative_skew_deviation_handler import RelativeSkewDeviationHandler
from raw_data.api.handlers.skew_handler import SkewHandler
from raw_data.api.handlers.vol_attenuation_handler import VolAttenuationHandler


def get_daily_returns_handler(postgres: PostgresClient, redis: RedisClient) -> DailyReturnsHandler:
    prices_client = get_daily_prices_client(postgres=postgres, redis=redis)
    return DailyReturnsHandler(prices_client=prices_client, redis=redis)


def get_daily_percentage_returns_handler(postgres: PostgresClient, redis: RedisClient) -> DailyPercentageReturnsHandler:
    prices_client = get_daily_prices_client(postgres=postgres, redis=redis)
    daily_returns_handler = get_daily_returns_handler(postgres=postgres, redis=redis)
    return DailyPercentageReturnsHandler(prices_client=prices_client, daily_returns_handler=daily_returns_handler)


def get_skew_handler(postgres: PostgresClient, redis: RedisClient) -> SkewHandler:
    daily_percentage_returns_handler = get_daily_percentage_returns_handler(postgres=postgres, redis=redis)
    return SkewHandler(
        daily_percentage_returns_handler=daily_percentage_returns_handler,
        redis=redis,
    )


def get_negskew_over_instrument_list_handler(postgres: PostgresClient, redis: RedisClient) -> NegSkewOverInstrumentListHandler:
    skew_handler = get_skew_handler(postgres=postgres, redis=redis)
    return NegSkewOverInstrumentListHandler(skew_handler=skew_handler)


def get_negskew_all_instruments_handler(postgres: PostgresClient, redis: RedisClient) -> NegSkewAllInstrumentsHandler:
    instruments_client = get_instruments_client(postgres=postgres)
    negskew_over_instrument_list_handler = get_negskew_over_instrument_list_handler(postgres=postgres, redis=redis)
    return NegSkewAllInstrumentsHandler(
        instruments_client=instruments_client,
        negskew_over_instrument_list_handler=negskew_over_instrument_list_handler,
    )


def get_current_average_negskew_over_all_assets_handler(
    postgres: PostgresClient, redis: RedisClient
) -> CurrentAverageNegSkewOverAllAssetsHandler:
    negskew_all_instruments_handler = get_negskew_all_instruments_handler(postgres=postgres, redis=redis)
    return CurrentAverageNegSkewOverAllAssetsHandler(negskew_all_instruments_handler=negskew_all_instruments_handler)


def get_historic_average_negskew_all_assets_handler(postgres: PostgresClient, redis: RedisClient) -> HistoricAverageNegSkewAllAssetsHandler:
    current_average_negskew_over_all_assets_handler = get_current_average_negskew_over_all_assets_handler(postgres=postgres, redis=redis)
    return HistoricAverageNegSkewAllAssetsHandler(
        current_average_negskew_over_all_assets_handler=current_average_negskew_over_all_assets_handler
    )


def get_absolute_skew_deviation_handler(postgres: PostgresClient, redis: RedisClient) -> AbsoluteSkewDeviationHandler:
    historic_negskew_value_all_assets_handler = get_historic_average_negskew_all_assets_handler(postgres=postgres, redis=redis)
    skew_handler = get_skew_handler(postgres=postgres, redis=redis)
    return AbsoluteSkewDeviationHandler(
        historic_negskew_value_all_assets_handler=historic_negskew_value_all_assets_handler,
        skew_handler=skew_handler,
    )


def get_fx_prices_handler(postgres: PostgresClient, redis: RedisClient) -> FxPricesHandler:
    instruments_client = get_instruments_client(postgres=postgres)
    prices_client = get_daily_prices_client(postgres=postgres, redis=redis)
    return FxPricesHandler(instruments_client=instruments_client, prices_client=prices_client)


def get_daily_returns_vol_handler(postgres: PostgresClient, redis: RedisClient) -> DailyReturnsVolHandler:
    prices_client = get_daily_prices_client(postgres=postgres, redis=redis)
    daily_returns_handler = get_daily_returns_handler(postgres=postgres, redis=redis)
    return DailyReturnsVolHandler(prices_client=prices_client, redis=redis, daily_returns_handler=daily_returns_handler)


def get_daily_percentage_volatility_handler(postgres: PostgresClient, redis: RedisClient) -> DailyPercentageVolatilityHandler:
    prices_client = get_daily_prices_client(postgres=postgres, redis=redis)
    daily_returns_vol_handler = get_daily_returns_vol_handler(postgres=postgres, redis=redis)
    return DailyPercentageVolatilityHandler(
        prices_client=prices_client,
        redis_repository=redis,
        daily_returns_vol_handler=daily_returns_vol_handler,
    )


def get_instrument_currency_vol_handler(postgres: PostgresClient, redis: RedisClient) -> InstrumentCurrencyVolHandler:
    prices_client = get_daily_prices_client(postgres=postgres, redis=redis)
    instruments_client = get_instruments_client(postgres=postgres)
    daily_percentage_volatility_handler = get_daily_percentage_volatility_handler(postgres=postgres, redis=redis)
    return InstrumentCurrencyVolHandler(
        prices_client=prices_client,
        instruments_client=instruments_client,
        daily_percentage_volatility_handler=daily_percentage_volatility_handler,
    )


def get_vol_attenuation_handler(postgres: PostgresClient, redis: RedisClient) -> VolAttenuationHandler:
    daily_percentage_volatility_handler = get_daily_percentage_volatility_handler(postgres=postgres, redis=redis)
    return VolAttenuationHandler(daily_percentage_volatility_handler=daily_percentage_volatility_handler, redis=redis)


def get_current_average_negskew_over_asset_class_handler(
    postgres: PostgresClient, redis: RedisClient
) -> CurrentAverageNegSkewOverAssetClassHandler:
    instruments_client = get_instruments_client(postgres=postgres)
    negskew_over_instrument_list_handler = get_negskew_over_instrument_list_handler(postgres=postgres, redis=redis)
    return CurrentAverageNegSkewOverAssetClassHandler(
        instruments_client=instruments_client, negskew_over_instrument_list_handler=negskew_over_instrument_list_handler
    )


def get_average_neg_skew_in_asset_class_for_instrument_handler(
    postgres: PostgresClient,
    redis: RedisClient,
) -> AverageNegSkewInAssetClassForInstrumentHandler:
    instruments_client = get_instruments_client(postgres=postgres)
    current_average_negskew_over_asset_class_handler = get_current_average_negskew_over_asset_class_handler(postgres=postgres, redis=redis)
    return AverageNegSkewInAssetClassForInstrumentHandler(
        instruments_client=instruments_client,
        current_average_negskew_over_asset_class_handler=current_average_negskew_over_asset_class_handler,
    )


def get_relative_skew_deviation_handler(postgres: PostgresClient, redis: RedisClient) -> RelativeSkewDeviationHandler:
    average_neg_skew_in_asset_class_for_instrument_handler = get_average_neg_skew_in_asset_class_for_instrument_handler(
        postgres=postgres, redis=redis
    )
    skew_handler = get_skew_handler(postgres=postgres, redis=redis)
    return RelativeSkewDeviationHandler(
        average_neg_skew_in_asset_class_for_instrument_handler=average_neg_skew_in_asset_class_for_instrument_handler,
        skew_handler=skew_handler,
    )
