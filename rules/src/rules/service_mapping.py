from collections.abc import Callable
from typing import Any

from common.protobufs.accel_pb2_grpc import add_AccelServicer_to_server
from common.protobufs.asserttrend_pb2_grpc import add_AssertTrendServicer_to_server
from common.protobufs.breakout_pb2_grpc import add_BreakoutServicer_to_server
from common.protobufs.carry_pb2_grpc import add_CarryServicer_to_server
from common.protobufs.cs_mean_reversion_pb2_grpc import add_CSMeanReversionServicer_to_server

from rules.api.dependencies.endpoints import EndpointFactory


async def create_service_mapping() -> dict[Callable[[Any, Any], None], Any]:
    """
    Creates a mapping of gRPC service registration methods to handler instances.

    Returns:
        A dictionary mapping gRPC service registration functions to handler instances.
    """
    endpoints_factory = EndpointFactory()
    # Initialize endpoints
    accel = endpoints_factory.get_accel()
    asserttrend = endpoints_factory.get_asserttrend()
    breakout = endpoints_factory.get_breakout()
    carry = endpoints_factory.get_carry()
    cs_mean_reversion = endpoints_factory.get_csmeanreversion()

    # Build the service mapping
    return {
        add_AccelServicer_to_server: accel,
        add_AssertTrendServicer_to_server: asserttrend,
        add_BreakoutServicer_to_server: breakout,
        add_CarryServicer_to_server: carry,
        add_CSMeanReversionServicer_to_server: cs_mean_reversion,
    }
