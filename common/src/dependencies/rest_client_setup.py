from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import FastAPI
from httpx import AsyncClient

from common.src.logging.logger import AppLogger

logger = AppLogger.get_instance().get_logger()


@lru_cache()
@asynccontextmanager
async def setup_async_client(app: FastAPI):
    app.state.requests_client = AsyncClient()
    yield
    await app.state.requests_client.aclose()
