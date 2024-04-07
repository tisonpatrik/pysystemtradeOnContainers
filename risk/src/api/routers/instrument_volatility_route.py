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


@router.get("/get_instrument_vol_by_symbol/", status_code=status.HTTP_200_OK, name="test_route")
async def get_instrument_vol_by_symbol(
    query: SymbolQuery = Depends(),  # Use Depends to inject the query parameters validated by Pydantic
    instrument_vol_handler: InstrumentVolHandler = Depends(get_instrument_vol_handler),
):
    try:
        symbol = query.symbol
        return await instrument_vol_handler.get_instrument_vol_for_symbol_async(symbol)
    except HTTPException as e:
        logger.error(f"An error occurred while trying to fetch FX rate for symbol {symbol}. Error: {e.detail}")
        return {"error": e.detail, "status_code": e.status_code}
    except ValidationError as e:
        logger.error(f"Validation error for symbol. Error: {e.json()}")
        return {"error": "Validation error", "details": e.errors(), "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY}
