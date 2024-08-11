from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
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
        daily_returns_vol = await daily_annualised_roll.get_daily_annualised_roll_async(query.symbol)
        return jsonable_encoder(daily_returns_vol)
    except HTTPException as e:
        logger.error(f"An error occurred while trying to fetch daily annualised roll for symbol {query.symbol}. Error: {e.detail}")
        return {"error": e.detail, "status_code": e.status_code}
    except ValidationError as e:
        logger.error(f"Validation error for symbol. Error: {e.json()}")
        return {"error": "Validation error", "details": e.errors(), "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY}
    except Exception as e:
        logger.error(f"Unhandled exception for symbol {query.symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
