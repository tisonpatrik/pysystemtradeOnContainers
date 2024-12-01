from collections.abc import Callable
from typing import Any

from common.protobufs.rules_processor_pb2_grpc import add_RulesProcessorServicer_to_server

from rules.dependencies.endpoints import EndpointFactory


async def create_service_mapping() -> dict[Callable[[Any, Any], None], Any]:
    """
    Creates a mapping of gRPC service registration methods to handler instances.

    Returns:
        A dictionary mapping gRPC service registration functions to handler instances.
    """
    endpoints_factory = EndpointFactory()

    rules_processor = endpoints_factory.get_rules_processor()
    # Build the service mapping
    return {
        add_RulesProcessorServicer_to_server: rules_processor,
    }
