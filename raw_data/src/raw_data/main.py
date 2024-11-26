import asyncio

from common.grpc.grpc_server import GRPCServer
from common.logging.logger import AppLogger
from raw_data.service_mapping import create_service_mapping

logger = AppLogger.get_instance().get_logger()


async def main() -> None:
    grpc_server = GRPCServer()
    service_mapping = None
    port = 50051

    try:
        # Initialize service mapping
        service_mapping = await create_service_mapping()

        # Start gRPC server
        await grpc_server.run_server_async(port, service_mapping)
        await grpc_server.wait_for_termination_async()
    except Exception:
        logger.exception("Unexpected error in gRPC server lifecycle.")
    finally:
        # Stop gRPC server and cleanup resources
        grace = 1
        await grpc_server.stop_server_async(grace)
        if service_mapping:
            for handler in service_mapping.values():
                if hasattr(handler, "close"):
                    await handler.close()
        logger.info("Server shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
