from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.cqrs.api_queries.rule_queries.get_assettrend import GetAssetTrendQuery
from common.logging.logger import AppLogger
from rules.api.dependencies.dependencies import get_asserttrend_handler
from rules.api.handlers.assettrend_handler import AssettrendHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_assettrend/",
    status_code=status.HTTP_200_OK,
    name="Get Assettrend",
)
async def get_breakout_async(
    query: GetAssetTrendQuery = Depends(),
    handler: AssettrendHandler = Depends(get_asserttrend_handler),
):
    try:
        result = await handler.get_assettrend_async(query)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result
    except HTTPException as e:
        logger.exception("An error occurred while trying to calculate accel for symbol %s. Error: %s", query.symbol, e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
