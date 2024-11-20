from collections.abc import Callable
from typing import Any

from common.src.protobufs.absolute_skew_deviation_pb2_grpc import (
    add_AbsoluteSkewDeviationHandlerServicer_to_server,
)
from raw_data.dependencies import get_absolute_skew_deviation_handler


def create_service_mapping() -> dict[Callable[[Any, Any], None], Any]:
    """
    Creates a mapping of gRPC service registration methods to handler instances.

    Returns:
        A dictionary mapping gRPC service registration functions to handler instances.
    """
    # Initialize service handlers
    absolute_skew_deviation_handler = get_absolute_skew_deviation_handler()

    # Build the service mapping
    return {
        add_AbsoluteSkewDeviationHandlerServicer_to_server: absolute_skew_deviation_handler,
        # Add other services here as needed
    }
