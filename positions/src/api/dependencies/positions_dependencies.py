from fastapi import Depends, Request

from common.src.database.repository import Repository
from positions.src.services.instrument_value_vol_service import InstrumentValueVolService


def get_repository(request: Request) -> Repository:
    return Repository(request.app.async_pool)


def get_instrument_value_vol_service(
    repository: Repository = Depends(get_repository),
) -> InstrumentValueVolService:
    return InstrumentValueVolService(repository)
