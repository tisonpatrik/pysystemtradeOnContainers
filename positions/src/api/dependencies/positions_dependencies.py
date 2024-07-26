from fastapi import Depends

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_client, get_repository
from common.src.http_client.rest_client import RestClient
from positions.src.api.handlers.positions_handler import PositionsHandler


async def get_positions_handler(
    db_repository: Repository = Depends(get_repository),
    client: RestClient = Depends(get_client),
) -> PositionsHandler:
    return PositionsHandler(repository=db_repository, client=client)
