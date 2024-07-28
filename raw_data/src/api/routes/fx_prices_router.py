from fastapi import APIRouter, Depends, HTTPException, status

from common.src.cqrs.api_queries.get_fx_rate import GetFxRateQuery
from common.src.logging.logger import AppLogger
from raw_data.src.api.dependencies.dependencies import get_fx_prices_handler
from raw_data.src.api.handlers.fx_prices_handler import FxPricesHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_fx_rate_by_symbol/",
    status_code=status.HTTP_200_OK,
    name="Get Config Data",
)
async def get_fx_rate_for_instrument(
    query: GetFxRateQuery = Depends(),
    fx_prices_handler: FxPricesHandler = Depends(get_fx_prices_handler),
):
    try:
        logger.info(f"Fetching FX rate for symbol: {query.symbol}")
        fx_rate = await fx_prices_handler.get_fx_prices_for_symbol_async(query)
        if fx_rate is None:
            logger.warning(f"FX rate not found for symbol: {query.symbol}")
            return {"message": "FX rate not found", "symbol": query.symbol}, status.HTTP_204_NO_CONTENT

        logger.info(f"Successfully fetched FX rate for symbol: {query.symbol}")
        return fx_rate
    except HTTPException as e:
        logger.error(f"Error fetching FX rate for symbol: {query.symbol}, Error: {str(e)}")
        return {"message": "Internal server error", "error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
