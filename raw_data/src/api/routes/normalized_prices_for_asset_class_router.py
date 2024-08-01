from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from common.src.cqrs.api_queries.get_normalized_price_for_asset_class_query import NormalizedPriceForAssetClassQuery
from common.src.logging.logger import AppLogger
from raw_data.src.api.dependencies.dependencies import get_normalized_price_for_asset_class_handler
from raw_data.src.api.handlers.normalize_prices_for_asset_class_handler import NormalizedPricesForAssetClassHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_normalized_price_for_asset_class/",
    status_code=status.HTTP_200_OK,
    name="Get Normalized Price For Asset Class",
)
async def get_normalized_price_for_asset_class(
    query: NormalizedPriceForAssetClassQuery = Depends(),
    normalizedPriceHandler: NormalizedPricesForAssetClassHandler = Depends(get_normalized_price_for_asset_class_handler),
):
    try:
        logger.info(f"Fetching normalized prices for asset class for symbol: {query.symbol}")
        normalized_price = await normalizedPriceHandler.get_normalized_price_for_asset_class_async(query)
        return jsonable_encoder(normalized_price)
    except HTTPException as e:
        logger.error(f"Error fetching normalized prices for asset class for symbol: {query.symbol}, Error: {str(e)}")
        return {"message": "Internal server error", "error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
