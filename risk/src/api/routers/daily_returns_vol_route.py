from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_daily_returns_vol import GetDailyReturnsVolQuery
from common.src.logging.logger import AppLogger
from risk.src.api.dependencies.risk_dependencies import get_daily_returns_vol_handler
from risk.src.api.handlers.daily_returns_volatility_handler import DailyReturnsVolHandler

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
        daily_returns_vol = await daily_returns_vol_handler.get_daily_returns_vol_async(query)
        return daily_returns_vol.to_json(orient="records")
    except HTTPException as e:
        logger.error(f"An error occurred while trying to fetch daily returns vol for symbol {query.symbol}. Error: {e.detail}")
        return {"error": e.detail, "status_code": e.status_code}
    except ValidationError as e:
        logger.error(f"Validation error for symbol. Error: {e.json()}")
        return {"error": "Validation error", "details": e.errors(), "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY}
    except Exception as e:
        logger.error(f"Unhandled exception for symbol {query.symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
