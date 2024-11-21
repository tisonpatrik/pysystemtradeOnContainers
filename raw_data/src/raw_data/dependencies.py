from common.src.clients.dependencies import (
    get_daily_prices_client_async,
    get_instruments_client_async,
    get_redis_async,
)
from raw_data.api.handlers.absolute_skew_deviation_handler import AbsoluteSkewDeviationHandler
from raw_data.api.handlers.current_average_negskew_over_all_assets_handler import (
    CurrentAverageNegSkewOverAllAssetsHandler,
)
from raw_data.api.handlers.daily_percentage_returns_handler import DailyPercentageReturnsHandler
from raw_data.api.handlers.daily_returns_handler import DailyReturnsHandler
from raw_data.api.handlers.historic_average_negskew_all_assets_handler import (
    HistoricAverageNegSkewAllAssetsHandler,
)
from raw_data.api.handlers.neg_skew_all_instruments_handler import NegSkewAllInstrumentsHandler
from raw_data.api.handlers.negskew_over_instrument_list_handler import NegSkewOverInstrumentListHandler
from raw_data.api.handlers.skew_handler import SkewHandler


async def get_daily_returns_handler() -> DailyReturnsHandler:
    prices_client = await get_daily_prices_client_async()
    redis_repository = await get_redis_async()
    return DailyReturnsHandler(prices_client=prices_client, redis_repository=redis_repository)


async def get_daily_percentage_returns_handler() -> DailyPercentageReturnsHandler:
    prices_client = await get_daily_prices_client_async()
    daily_returns_handler = await get_daily_returns_handler()
    return DailyPercentageReturnsHandler(prices_client=prices_client, daily_returns_handler=daily_returns_handler)


async def get_skew_handler() -> SkewHandler:
    daily_percentage_returns_handler = await get_daily_percentage_returns_handler()
    redis_repository = await get_redis_async()
    return SkewHandler(
        daily_percentage_returns_handler=daily_percentage_returns_handler,
        redis_repository=redis_repository,
    )


async def get_negskew_over_instrument_list_handler() -> NegSkewOverInstrumentListHandler:
    skew_handler = await get_skew_handler()
    return NegSkewOverInstrumentListHandler(skew_handler=skew_handler)


async def get_negskew_all_instruments_handler() -> NegSkewAllInstrumentsHandler:
    instruments_client = await get_instruments_client_async()
    negskew_over_instrument_list_handler = await get_negskew_over_instrument_list_handler()
    return NegSkewAllInstrumentsHandler(
        instruments_client=instruments_client,
        negskew_over_instrument_list_handler=negskew_over_instrument_list_handler,
    )


async def get_current_average_negskew_over_all_assets_handler() -> CurrentAverageNegSkewOverAllAssetsHandler:
    negskew_all_instruments_handler = await get_negskew_all_instruments_handler()
    return CurrentAverageNegSkewOverAllAssetsHandler(negskew_all_instruments_handler=negskew_all_instruments_handler)


async def get_historic_average_negskew_all_assets_handler() -> HistoricAverageNegSkewAllAssetsHandler:
    current_average_negskew_over_all_assets_handler = await get_current_average_negskew_over_all_assets_handler()
    return HistoricAverageNegSkewAllAssetsHandler(
        current_average_negskew_over_all_assets_handler=current_average_negskew_over_all_assets_handler
    )


async def get_absolute_skew_deviation_handler() -> AbsoluteSkewDeviationHandler:
    historic_negskew_value_all_assets_handler = await get_historic_average_negskew_all_assets_handler()
    skew_handler = await get_skew_handler()
    return AbsoluteSkewDeviationHandler(
        historic_negskew_value_all_assets_handler=historic_negskew_value_all_assets_handler,
        skew_handler=skew_handler,
    )
