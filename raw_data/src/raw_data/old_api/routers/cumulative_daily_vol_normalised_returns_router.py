from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.raw_data_queries.get_cumulative_daily_vol_norm_returns import CumulativeDailyVolNormReturnsQuery
from common.src.logging.logger import AppLogger
from raw_data.old_api.dependencies.dependencies import get_cumulative_daily_vol_norm_returns_handler
from raw_data.src.raw_data.api.handlers.cumulative_daily_vol_norm_returns_handler import CumulativeDailyVolNormReturnsHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_cum_daily_vol_normalised_returns/",
    status_code=status.HTTP_200_OK,
    name="Get cummulative daily vol normalised returns",
)
async def get_cum_daily_vol_normalised_returns(
    query: CumulativeDailyVolNormReturnsQuery = Depends(),
    handler: CumulativeDailyVolNormReturnsHandler = Depends(get_cumulative_daily_vol_norm_returns_handler),
):
    try:
        result = await handler.get_cumulative_daily_vol_normalized_returns_async(query.symbol)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result

    except HTTPException as e:
        logger.exception(
            "An error occurred while trying to get cummulative daily vol normalised returns for symbol %s. Error: %s",
            query.symbol,
            e.detail,
        )
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
