from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_forecast_for_symbol_query import GetForecastForSymbolQuery
from common.src.logging.logger import AppLogger
from forecast.api.dependencies.forecast_dependencies import get_raw_forecast_handler
from forecast.api.handlers.raw_forecast_handler import RawForecastHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_forecast_for_instrument_route/",
    status_code=status.HTTP_200_OK,
    name="Get raw forecast",
)
async def get_forecast_for_instrument_async(
    request: GetForecastForSymbolQuery = Depends(),
    instrument_vol_handler: RawForecastHandler = Depends(get_raw_forecast_handler),
):
    try:
        result = await instrument_vol_handler.get_raw_forecast_async(request)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result

    except HTTPException as e:
        logger.exception("An error occurred while trying to get forecast for symbol %s. Error: %s", request.symbol, e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", request.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
