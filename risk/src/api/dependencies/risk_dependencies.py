from fastapi import Depends

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_repository
from risk.src.api.handlers.instrument_currency_vol_handler import InstrumentCurrencyVolHandler


async def get_instrument_vol_handler(repository: Repository = Depends(get_repository)) -> InstrumentCurrencyVolHandler:
    return InstrumentCurrencyVolHandler(repository=repository)
