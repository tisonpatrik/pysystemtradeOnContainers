from fastapi import APIRouter, Depends, HTTPException, status

from common.src.logging.logger import AppLogger
from raw_data.src.api.handlers.fx_prices_handler import FxPricesHandler
from raw_data.src.dependencies.dependencies import get_fx_prices_handler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_fx_rate_by_symbol/{symbol}/",
    status_code=status.HTTP_200_OK,
    name="Get Config Data",
)
async def get_fx_rate_by_symbol(symbol: str, fx_prices_handler: FxPricesHandler = Depends(get_fx_prices_handler)):

    try:
        logger.info(f"Fetching FX rate for symbol: {symbol}")
        fx_rate = await fx_prices_handler.get_fx_prices_for_symbol_async(symbol)
        if fx_rate is None:
            logger.error(f"FX rate not found for symbol: {symbol}")
            raise HTTPException(status_code=404, detail="FX rate not found")

        logger.info(f"Successfully fetched FX rate for symbol: {symbol}")
        return fx_rate
    except Exception as e:
        logger.error(f"Error fetching FX rate for symbol: {symbol}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
