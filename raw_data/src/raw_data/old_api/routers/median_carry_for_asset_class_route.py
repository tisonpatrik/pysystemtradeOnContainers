from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.raw_data_queries.get_median_carry_for_asset_class import GetMedianCarryForAssetClassQuery
from common.src.logging.logger import AppLogger
from raw_data.old_api.dependencies.dependencies import get_median_carry_for_asset_class_handler
from raw_data.old_api.handlers.median_carry_for_asset_class_handler import MedianCarryForAssetClassHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_median_carry_for_asset_class/",
    status_code=status.HTTP_200_OK,
    name="Get median carry for asset class router",
)
async def get_median_carry_for_asset_class(
    query: GetMedianCarryForAssetClassQuery = Depends(),
    handler: MedianCarryForAssetClassHandler = Depends(get_median_carry_for_asset_class_handler),
):
    try:
        result = await handler.get_median_carry_for_asset_class_async(query.symbol)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result

    except HTTPException as e:
        logger.exception(
            "An error occurred while trying to get median carry for asset class for symbol %s. Error: %s", query.symbol, e.detail
        )
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
