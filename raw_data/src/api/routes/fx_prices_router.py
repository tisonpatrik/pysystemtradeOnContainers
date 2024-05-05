from fastapi import APIRouter, Depends, HTTPException, status

from common.src.logging.logger import AppLogger
from common.src.models.api_query_models import GetFxRateQuery
from raw_data.src.api.handlers.fx_prices_handler import FxPricesHandler
from raw_data.src.api.dependencies.dependencies import get_fx_prices_handler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_fx_rate_by_symbol/",
    status_code=status.HTTP_200_OK,
    name="Get Config Data",
)
async def get_fx_rate_for_instrument(
    query: GetFxRateQuery = Depends(),
    fx_prices_handler: FxPricesHandler = Depends(
        get_fx_prices_handler,
    ),
):
    try:
        logger.info(f"Fetching FX rate for symbol: {query.symbol}")
        fx_rate = await fx_prices_handler.get_fx_prices_for_symbol_async(query)
        if fx_rate is None:
            logger.error(f"FX rate not found for symbol: {query.symbol}")
            raise HTTPException(status_code=404, detail="FX rate not found")

        logger.info(f"Successfully fetched FX rate for symbol: {query.symbol}")
        return fx_rate
    except Exception as e:
        logger.error(f"Error fetching FX rate for symbol: {query.symbol}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
