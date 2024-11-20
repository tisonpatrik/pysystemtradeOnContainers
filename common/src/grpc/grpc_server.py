import grpc

from common.src.logging.logger import AppLogger


class GRPCServer:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.server = grpc.aio.server()

    async def run_server(self, port, service_mapping):
        try:
            for service_adder, servicer in service_mapping.items():
                service_adder(servicer, self.server)

            self.server.add_insecure_port(f"[::]:{port}")
            await self.server.start()
            self.logger.info("Server started and listening on port %s", port)
        except Exception:
            self.logger.exception("Failed to start server on port %s:", port)
            raise

    async def stop_server(self, grace=0):
        try:
            await self.server.stop(grace)
            self.logger.info("Server stopped successfully")
        except Exception:
            self.logger.exception("Error while stopping the server")
            raise

    async def wait_for_termination(self):
        try:
            await self.server.wait_for_termination()
            self.logger.info("Server has terminated")
        except Exception:
            self.logger.exception("Error while waiting for server termination:")
            raise
