from fastapi import APIRouter, Depends, HTTPException, status

from common.src.cqrs.api_queries.get_normalized_price_for_asset_class_query import NormalizedPriceForAssetClassQuery
from common.src.logging.logger import AppLogger
from raw_data.src.api.dependencies.dependencies import get_normalized_price_for_asset_class_handler
from raw_data.src.api.handlers.normalize_price_for_asset_class_handler import NormalizedPriceForAssetClassHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_normalized_price_for_asset_class/",
    status_code=status.HTTP_200_OK,
    name="Get Normalized Price For Asset Class",
)
async def get_normalized_price_for_asset_class(
    query: NormalizedPriceForAssetClassQuery = Depends(),
    normalizedPriceHandler: NormalizedPriceForAssetClassHandler = Depends(get_normalized_price_for_asset_class_handler),
):
    try:
        logger.info("")
        fx_rate = await normalizedPriceHandler.get_normalized_price_for_asset_class_async(query)
        if fx_rate is None:
            logger.warning(f"FX rate not found for symbol: {query.symbol}")
            return {"message": "FX rate not found", "symbol": query.symbol}, status.HTTP_204_NO_CONTENT

        logger.info(f"Successfully fetched normalized prices for asset class for symbol: {query.symbol}")
        return fx_rate
    except HTTPException as e:
        logger.error(f"Error fetching normalized prices for asset class for symbol: {query.symbol}, Error: {str(e)}")
        return {"message": "Internal server error", "error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
