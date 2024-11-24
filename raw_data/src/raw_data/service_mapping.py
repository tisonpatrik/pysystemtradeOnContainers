from collections.abc import Callable
from typing import Any

from common.src.clients.dependencies import get_database_async, get_redis
from common.src.protobufs.absolute_skew_deviation_pb2_grpc import (
    add_AbsoluteSkewDeviationServicer_to_server,
)
from common.src.protobufs.fx_prices_pb2_grpc import add_FxPricesServicer_to_server
from raw_data.api.dependencies.endpoints import get_absolute_skew_deviation, get_fx_prices


async def create_service_mapping() -> dict[Callable[[Any, Any], None], Any]:
    """
    Creates a mapping of gRPC service registration methods to handler instances.

    Returns:
        A dictionary mapping gRPC service registration functions to handler instances.
    """
    redis = get_redis()
    postgres = await get_database_async()
    # Initialize endpoints
    absolute_skew_deviation_handler = get_absolute_skew_deviation(postgres, redis)
    fx_prices_handler = get_fx_prices(postgres, redis)

    # Build the service mapping
    return {
        add_AbsoluteSkewDeviationServicer_to_server: absolute_skew_deviation_handler,
        add_FxPricesServicer_to_server: fx_prices_handler,
    }
