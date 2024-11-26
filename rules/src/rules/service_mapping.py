from collections.abc import Callable
from typing import Any

from common.protobufs.accel_pb2_grpc import add_AccelServicer_to_server
from common.protobufs.asserttrend_pb2_grpc import add_AssertTrendServicer_to_server

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

    # Build the service mapping
    return {
        add_AccelServicer_to_server: accel,
        add_AssertTrendServicer_to_server: asserttrend,
    }
