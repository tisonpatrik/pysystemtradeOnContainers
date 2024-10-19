from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_instrument_currency_vol import GetInstrumentCurrencyVolQuery
from common.src.logging.logger import AppLogger
from raw_data.src.api.dependencies.dependencies import get_instrument_vol_handler
from raw_data.src.api.handlers.instrument_currency_vol_handler import InstrumentCurrencyVolHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_instrument_currency_volatility/",
    status_code=status.HTTP_200_OK,
    name="Get instrument currency volatility",
)
async def get_instrument_currency_volalitlty_async(
    query: GetInstrumentCurrencyVolQuery = Depends(),
    handler: InstrumentCurrencyVolHandler = Depends(get_instrument_vol_handler),
):
    try:
        result = await handler.get_instrument_vol_for_symbol_async(query)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result
    except HTTPException as e:
        logger.exception(
            "An error occurred while trying to get instrument currency volatility for symbol %s. Error: %s", query.symbol, e.detail
        )
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
