from collections.abc import Callable
from typing import Any

from common.src.clients.dependencies import get_database_async, get_redis
from common.src.protobufs.absolute_skew_deviation_pb2_grpc import (
    add_AbsoluteSkewDeviationServicer_to_server,
)
from common.src.protobufs.cumulative_daily_vol_norm_returns_pb2_grpc import add_CumulativeDailyVolNormReturnsServicer_to_server
from common.src.protobufs.daily_returns_vol_pb2_grpc import add_DailyReturnsVolServicer_to_server
from common.src.protobufs.fx_prices_pb2_grpc import add_FxPricesServicer_to_server
from common.src.protobufs.instrument_currency_vol_pb2_grpc import add_InstrumentCurrencyVolServicer_to_server
from common.src.protobufs.median_carry_for_asset_class_pb2_grpc import add_MedianCarryServicer_to_server
from common.src.protobufs.raw_carry_pb2_grpc import add_RawCarryServicer_to_server
from common.src.protobufs.relative_skew_deviation_pb2_grpc import add_RelativeSkewDeviationServicer_to_server
from common.src.protobufs.smooth_carry_pb2_grpc import add_SmoothCarryServicer_to_server
from common.src.protobufs.vol_attenuation_pb2_grpc import add_VolAttenuationServicer_to_server
from raw_data.api.dependencies.endpoints import (
    get_absolute_skew_deviation,
    get_cumulative_daily_vol_norm_returns,
    get_daily_returns_vol,
    get_fx_prices,
    get_instrument_currency_vol,
    get_median_carry_for_asset_class,
    get_raw_carry,
    get_relative_skew_deviation,
    get_smooth_carry,
    get_vol_attenuation,
)


async def create_service_mapping() -> dict[Callable[[Any, Any], None], Any]:
    """
    Creates a mapping of gRPC service registration methods to handler instances.

    Returns:
        A dictionary mapping gRPC service registration functions to handler instances.
    """
    redis = get_redis()
    postgres = await get_database_async()
    # Initialize endpoints
    absolute_skew_deviation = get_absolute_skew_deviation(postgres, redis)
    cumulative_daily_vol_norm_returns = get_cumulative_daily_vol_norm_returns(postgres, redis)
    daily_returns_vol = get_daily_returns_vol(postgres, redis)
    fx_prices = get_fx_prices(postgres, redis)
    instrument_currency_vol = get_instrument_currency_vol(postgres, redis)
    median_carry_for_asset_class = get_median_carry_for_asset_class(postgres, redis)
    raw_carry = get_raw_carry(postgres, redis)

    relative_skew_deviation = get_relative_skew_deviation(postgres, redis)
    smooth_carry = get_smooth_carry(postgres, redis)
    vol_attenuation = get_vol_attenuation(postgres, redis)

    # Build the service mapping
    return {
        add_AbsoluteSkewDeviationServicer_to_server: absolute_skew_deviation,
        add_CumulativeDailyVolNormReturnsServicer_to_server: cumulative_daily_vol_norm_returns,
        add_DailyReturnsVolServicer_to_server: daily_returns_vol,
        add_FxPricesServicer_to_server: fx_prices,
        add_InstrumentCurrencyVolServicer_to_server: instrument_currency_vol,
        add_MedianCarryServicer_to_server: median_carry_for_asset_class,
        add_RawCarryServicer_to_server: raw_carry,
        add_RelativeSkewDeviationServicer_to_server: relative_skew_deviation,
        add_SmoothCarryServicer_to_server: smooth_carry,
        add_VolAttenuationServicer_to_server: vol_attenuation,
    }
