# grpc_channel.py

import asyncio

import grpc
from grpc import StatusCode
from grpc.aio import Channel

from common.app_settings import GRPC_CHANNEL_RETRIES, GRPC_CHANNEL_RETRY_DELAY
from common.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()


async def setup_grpc_channel(target_address: str) -> Channel:
    retries = GRPC_CHANNEL_RETRIES
    delay = GRPC_CHANNEL_RETRY_DELAY
    target_address = 'pysystemtradeoncontainers-raw_data-1:50051'

    channel = grpc.aio.insecure_channel(target_address)
    for attempt in range(retries):
        try:
            await channel.channel_ready()
            logger.info('gRPC channel to %s was successfully initialized.', target_address)
            return channel
        except grpc.aio.AioRpcError as e:
            logger.warning(
                'gRPC channel to %s failed. Code: %s, Details: %s',
                target_address,
                e.code(),
                e.details(),
            )
            if e.code() == StatusCode.UNAVAILABLE:
                logger.warning('Retrying in %d seconds...', delay)
                await asyncio.sleep(delay)
            else:
                raise

        except Exception as e:
            logger.exception('Unexpected error during gRPC channel initialization: %s', e)
            raise

    logger.error('Unable to establish gRPC channel to %s after %d attempts.', target_address, retries)
    raise Exception(f'Unable to establish gRPC channel to {target_address} after {retries} attempts.')
