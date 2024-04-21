from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, StringConstraints, ValidationError
from typing_extensions import Annotated

from common.src.logging.logger import AppLogger
from risk.src.api.handlers.instrument_volatility_handler import InstrumentVolHandler
from risk.src.dependencies.risk_dependencies import get_instrument_vol_handler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


class SymbolQuery(BaseModel):
    symbol: Annotated[str, StringConstraints(max_length=10)]
    base_currency: Annotated[str, StringConstraints(max_length=3)]
    annual_cash_vol_target: float


@router.get(
    "/get_average_position_at_subsystem_level/",
    status_code=status.HTTP_200_OK,
    name="get_average_position_at_subsystem_level",
)
async def get_average_position_at_subsystem_level(
    query: SymbolQuery = Depends(),
    instrument_vol_handler: InstrumentVolHandler = Depends(get_instrument_vol_handler),
):
    try:
        instr_value_vol = await instrument_vol_handler.get_instrument_vol_for_symbol_async(
            query.symbol, query.base_currency
        )

        vol_scalar = query.annual_cash_vol_target / instr_value_vol
        return vol_scalar.tail()
    except HTTPException as e:
        logger.error(
            f"An error occurred while trying to fetch instrument volatility for symbol {query.symbol}. Error: {e.detail}"
        )
        return {"error": e.detail, "status_code": e.status_code}
    except ValidationError as e:
        logger.error(f"Validation error for symbol. Error: {e.json()}")
        return {"error": "Validation error", "details": e.errors(), "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY}
