from collections.abc import Callable
from typing import Any

from common.protobufs.absolute_skew_deviation_pb2_grpc import (
    add_AbsoluteSkewDeviationServicer_to_server,
)
from common.protobufs.cumulative_daily_vol_norm_returns_pb2_grpc import add_CumulativeDailyVolNormReturnsServicer_to_server
from common.protobufs.daily_returns_vol_pb2_grpc import add_DailyReturnsVolServicer_to_server
from common.protobufs.fx_prices_pb2_grpc import add_FxPricesServicer_to_server
from common.protobufs.instrument_currency_vol_pb2_grpc import add_InstrumentCurrencyVolServicer_to_server
from common.protobufs.median_carry_for_asset_class_pb2_grpc import add_MedianCarryServicer_to_server
from common.protobufs.normalized_prices_pb2_grpc import add_NormalizedPricesServicer_to_server
from common.protobufs.raw_carry_pb2_grpc import add_RawCarryServicer_to_server
from common.protobufs.relative_skew_deviation_pb2_grpc import add_RelativeSkewDeviationServicer_to_server
from common.protobufs.smooth_carry_pb2_grpc import add_SmoothCarryServicer_to_server
from common.protobufs.vol_attenuation_pb2_grpc import add_VolAttenuationServicer_to_server

from raw_data.api.dependencies.endpoints import EndpointFactory


async def create_service_mapping() -> dict[Callable[[Any, Any], None], Any]:
    """
    Creates a mapping of gRPC service registration methods to handler instances.

    Returns:
        A dictionary mapping gRPC service registration functions to handler instances.
    """
    endpoint_factory = await EndpointFactory.create()
    # Initialize endpoints
    absolute_skew_deviation = endpoint_factory.get_absolute_skew_deviation()
    cumulative_daily_vol_norm_returns = endpoint_factory.get_cumulative_daily_vol_norm_returns()
    daily_returns_vol = endpoint_factory.get_daily_returns_vol()
    fx_prices = endpoint_factory.get_fx_prices()
    instrument_currency_vol = endpoint_factory.get_instrument_currency_vol()
    median_carry_for_asset_class = endpoint_factory.get_median_carry_for_asset_class()
    normalized_prices = endpoint_factory.get_normalized_prices()
    raw_carry = endpoint_factory.get_raw_carry()
    relative_skew_deviation = endpoint_factory.get_relative_skew_deviation()
    smooth_carry = endpoint_factory.get_smooth_carry()
    vol_attenuation = endpoint_factory.get_vol_attenuation()

    # Build the service mapping
    return {
        add_AbsoluteSkewDeviationServicer_to_server: absolute_skew_deviation,
        add_CumulativeDailyVolNormReturnsServicer_to_server: cumulative_daily_vol_norm_returns,
        add_DailyReturnsVolServicer_to_server: daily_returns_vol,
        add_FxPricesServicer_to_server: fx_prices,
        add_InstrumentCurrencyVolServicer_to_server: instrument_currency_vol,
        add_MedianCarryServicer_to_server: median_carry_for_asset_class,
        add_NormalizedPricesServicer_to_server: normalized_prices,
        add_RawCarryServicer_to_server: raw_carry,
        add_RelativeSkewDeviationServicer_to_server: relative_skew_deviation,
        add_SmoothCarryServicer_to_server: smooth_carry,
        add_VolAttenuationServicer_to_server: vol_attenuation,
    }
