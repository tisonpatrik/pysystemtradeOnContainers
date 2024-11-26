import asyncio
from typing import Any

import grpc

from common.logging.logger import AppLogger


class GRPCServer:
    def __init__(self) -> None:
        self.logger = AppLogger.get_instance().get_logger()
        self.server = grpc.aio.server()

    async def run_server_async(self, port: int, service_mapping: dict[(Any, Any)]) -> None:
        try:
            for service_adder, servicer in service_mapping.items():
                service_adder(servicer, self.server)

            self.server.add_insecure_port(f'[::]:{port}')
            await self.server.start()
            self.logger.info('Server started and listening on port %s', port)
        except Exception:
            self.logger.exception('Failed to start server on port %s:', port)
            raise

    async def wait_for_termination_async(self) -> None:
        try:
            await self.server.wait_for_termination()
            self.logger.info('Server has terminated')
        except asyncio.CancelledError:
            self.logger.warning('Server termination was cancelled')
        except Exception:
            self.logger.exception('Error while waiting for server termination:')
            raise

    async def stop_server_async(self, grace: int) -> None:
        try:
            await self.server.stop(grace)
            self.logger.info('Server stopped successfully')
        except asyncio.CancelledError:
            self.logger.warning('Server shutdown was cancelled')
        except Exception:
            self.logger.exception('Error while stopping the server')
            raise
