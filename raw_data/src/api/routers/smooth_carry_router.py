from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_raw_carry import GetRawCarryQuery
from common.src.logging.logger import AppLogger
from raw_data.src.api.dependencies.dependencies import get_smooth_carry_handler
from raw_data.src.api.handlers.smooth_carry_handler import SmoothCarryHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_smooth_carry/",
    status_code=status.HTTP_200_OK,
    name="Get smooth carry router",
)
async def get_raw_carry_by_symbol(
    query: GetRawCarryQuery = Depends(),
    handler: SmoothCarryHandler = Depends(get_smooth_carry_handler),
):
    try:
        result = await handler.get_smooth_carry_async(query.symbol)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result

    except HTTPException as e:
        logger.exception("An error occurred while trying to get smooth carry for symbol %s. Error: %s", query.symbol, e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
