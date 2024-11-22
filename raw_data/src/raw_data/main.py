import asyncio

from common.src.clients.dependencies import get_database_async, get_redis
from common.src.grpc.grpc_server import GRPCServer
from common.src.logging.logger import AppLogger
from raw_data.service_mapping import create_service_mapping

logger = AppLogger.get_instance().get_logger()


async def main():
    grpc_server = GRPCServer()
    service_mapping = None
    port = 50051

    try:
        redis = get_redis()
        postgres = await get_database_async()
        # Initialize service mapping
        service_mapping = create_service_mapping(postgres=postgres, redis=redis)

        # Start gRPC server
        await grpc_server.run_server(port, service_mapping)
        await grpc_server.wait_for_termination()
    except Exception:
        logger.exception("Unexpected error in gRPC server lifecycle.")
    finally:
        # Stop gRPC server and cleanup resources
        await grpc_server.stop_server()
        if service_mapping:
            for handler in service_mapping.values():
                if hasattr(handler, "close"):
                    await handler.close()
        logger.info("Server shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
