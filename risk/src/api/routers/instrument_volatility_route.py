from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_instrument_currency_vol import GetInstrumentCurrencyVolQuery
from common.src.logging.logger import AppLogger
from risk.src.api.dependencies.risk_dependencies import get_instrument_vol_handler
from risk.src.api.handlers.instrument_currency_vol_handler import InstrumentCurrencyVolHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_instrument_currency_volatility/",
    status_code=status.HTTP_200_OK,
    name="get_instrument_currency_volatility",
)
async def get_instrument_currency_volalitlty_async(
    query: GetInstrumentCurrencyVolQuery = Depends(),
    instrument_vol_handler: InstrumentCurrencyVolHandler = Depends(get_instrument_vol_handler),
):
    try:
        instr_value_vol = await instrument_vol_handler.get_instrument_vol_for_symbol_async(query)
        return jsonable_encoder(instr_value_vol)

    except HTTPException as e:
        logger.error(f"An error occurred while trying to fetch instrument volatility for symbol {query.symbol}. Error: {e.detail}")
        return {"error": e.detail, "status_code": e.status_code}
    except ValidationError as e:
        logger.error(f"Validation error for symbol. Error: {e.json()}")
        return {"error": "Validation error", "details": e.errors(), "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY}
    except Exception as e:
        logger.error(f"Unhandled exception for symbol {query.symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
