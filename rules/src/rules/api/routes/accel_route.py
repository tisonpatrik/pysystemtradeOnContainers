from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.rule_queries.get_accel import GetAccelQuery
from common.src.logging.logger import AppLogger
from rules.api.dependencies.dependencies import get_accel_handler
from rules.api.handlers.accel_handler import AccelHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_accel/",
    status_code=status.HTTP_200_OK,
    name="Get Accel",
)
async def get_accel_async(
    query: GetAccelQuery = Depends(),
    accel_handler: AccelHandler = Depends(get_accel_handler),
):
    try:
        result = await accel_handler.get_accel_async(query)
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
