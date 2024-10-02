from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_daily_returns_vol import GetDailyReturnsVolQuery
from common.src.logging.logger import AppLogger
from raw_data.src.api.dependencies.dependencies import get_daily_returns_vol_handler
from raw_data.src.api.handlers.daily_returns_vol_handler import DailyReturnsVolHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_daily_returns_vol/",
    status_code=status.HTTP_200_OK,
    name="Get daily returns volatility",
)
async def get_daily_returns_vol(
    query: GetDailyReturnsVolQuery = Depends(),
    daily_returns_vol_handler: DailyReturnsVolHandler = Depends(get_daily_returns_vol_handler),
):
    try:
        result = await daily_returns_vol_handler.get_daily_returns_vol_async(query.symbol)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result

    except HTTPException as e:
        logger.exception("An error occurred while trying to get daily returns volatility for symbol %s. Error: %s", query.symbol, e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
