import asyncio

import grpc
from common.logging.logger import AppLogger

from raw_data.service_mapping import create_service_mapping

logger = AppLogger.get_instance().get_logger()


async def main() -> None:
    service_mapping = await create_service_mapping()
    port = 50051

    server = grpc.aio.server()
    try:
        for service_adder, servicer in service_mapping.items():
            service_adder(servicer, server)

        server.add_insecure_port(f'[::]:{port}')
        await server.start()
        logger.info('Server started and listening on port %s', port)
        await server.wait_for_termination()
    except Exception as e:
        logger.exception('Unexpected error in gRPC server lifecycle: %s', e)
    finally:
        grace = 1
        await server.stop(grace)
        logger.info('Server shutdown complete.')

        if service_mapping:
            for handler in service_mapping.values():
                if hasattr(handler, 'close'):
                    try:
                        await handler.close()
                    except Exception as e:
                        logger.exception('Failed to close handler %s: %s', handler, e)


if __name__ == '__main__':
    asyncio.run(main())
