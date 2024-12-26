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
    channel = grpc.aio.insecure_channel(target_address)
    for attempt in range(retries):
        try:
            await channel.channel_ready()
            logger.info('gRPC channel to %s was successfully initialized.', target_address)
            return channel
        except grpc.aio.AioRpcError as e:
            if e.code() == StatusCode.UNAVAILABLE:
                logger.warning(
                    'gRPC channel to %s is unavailable (attempt %d/%d). Retrying in %d seconds...',
                    target_address,
                    attempt + 1,
                    retries,
                    delay,
                )
                await asyncio.sleep(delay)
            else:
                logger.exception('gRPC error during channel initialization: %s', e)
                raise
        except Exception as e:
            logger.exception('Unexpected error during gRPC channel initialization: %s', e)
            raise
    raise Exception(f'Unable to establish gRPC channel to {target_address} after {retries} attempts.')
