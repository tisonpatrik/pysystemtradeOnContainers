from contextlib import asynccontextmanager

from fastapi import FastAPI

from common.src.dependencies.db_setup import setup_async_database


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_database(app):
        yield
