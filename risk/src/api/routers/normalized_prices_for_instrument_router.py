from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_normalized_price_for_instrument_query import GetNormalizedPriceForInstrumentQuery
from common.src.logging.logger import AppLogger
from risk.src.api.dependencies.dependencies import get_daily_vol_normalized_returns_handler
from risk.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_normalized_prices_for_instrument/",
    status_code=status.HTTP_200_OK,
    name="Get normalized price for instrument",
)
async def get_normalized_prices_for_instrument(
    query: GetNormalizedPriceForInstrumentQuery = Depends(),
    normalizedPriceHandler: DailyvolNormalizedReturnsHandler = Depends(get_daily_vol_normalized_returns_handler),
):
    try:
        result = await normalizedPriceHandler.get_daily_vol_normalized_returns(query.symbol)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result

    except HTTPException as e:
        logger.exception(
            "An error occurred while trying to get normalized price for instrument for symbol %s. Error: %s", query.symbol, e.detail
        )
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
