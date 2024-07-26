from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from rules_manager.src.api.handlers.rules_handler import RulesHandler

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_repository
from common.src.dependencies.db_setup import setup_async_database


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_database(app):
        yield


def get_rules_handler(repository: Repository = Depends(get_repository)) -> RulesHandler:
    return RulesHandler(repository=repository)
