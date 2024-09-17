from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_daily_annualised_roll import GetDailyAnnualisedRollQuery
from common.src.logging.logger import AppLogger
from raw_data.src.api.dependencies.dependencies import get_annualised_roll_handler
from raw_data.src.api.handlers.daily_annualised_roll_handler import DailyAnnualisedRollHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_daily_annualised_roll/",
    status_code=status.HTTP_200_OK,
    name="Get daily annualised roll router",
)
async def get_daily_annualised_roll_router(
    query: GetDailyAnnualisedRollQuery = Depends(),
    daily_annualised_roll: DailyAnnualisedRollHandler = Depends(get_annualised_roll_handler),
):
    try:
        result = await daily_annualised_roll.get_daily_annualised_roll_async(query.symbol)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result

    except HTTPException as e:
        logger.exception("An error occurred while trying to get daily annualised roll for symbol %s. Error: %s", query.symbol, e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
