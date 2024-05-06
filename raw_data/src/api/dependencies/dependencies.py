from fastapi import Depends

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_repository
from raw_data.src.api.handlers.fx_prices_handler import FxPricesHandler


def get_fx_prices_handler(repository: Repository = Depends(get_repository)) -> FxPricesHandler:
    return FxPricesHandler(repository=repository)
