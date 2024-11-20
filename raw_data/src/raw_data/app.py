import asyncio

from common.src.grpc.grpc_server import GRPCServer
from raw_data.src.raw_data.service_mapping import create_service_mapping


async def main():
    grpc_server = GRPCServer()
    service_mapping = create_service_mapping()
    port = 50051

    await grpc_server.run_server(port, service_mapping)
    await grpc_server.wait_for_termination()
    await grpc_server.stop_server()


if __name__ == "__main__":
    asyncio.run(main())
