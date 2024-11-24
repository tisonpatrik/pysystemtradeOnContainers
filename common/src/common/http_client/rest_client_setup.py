from httpx import AsyncClient

from common.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()


async def setup_async_client() -> AsyncClient:
    client = AsyncClient()
    try:
        logger.info("AsyncClient initialized.")
        return client
    finally:
        await client.aclose()
        logger.info("AsyncClient closed.")
