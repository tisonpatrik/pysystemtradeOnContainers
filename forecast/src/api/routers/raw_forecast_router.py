from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_forecast_for_symbol_query import GetForecastForSymbolQuery
from common.src.logging.logger import AppLogger
from forecast.src.api.dependencies.forecast_dependencies import get_raw_forecast_handler
from forecast.src.api.handlers.raw_forecast_handler import RawForecastHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_forecast_for_instrument_route/",
    status_code=status.HTTP_200_OK,
    name="Get raw forecast",
)
async def get_forecast_for_instrument_async(
    query: GetForecastForSymbolQuery = Depends(),
    instrument_vol_handler: RawForecastHandler = Depends(get_raw_forecast_handler),
):
    try:
        forecast = await instrument_vol_handler.get_raw_forecast_async(query)
        logger.info(f"Successfully fetched forecast: {forecast}")
        return forecast
    except HTTPException as e:
        logger.error(f"An error occurred while trying to fetch forecast. Error: {e.detail}")
        return {"error": e.detail, "status_code": e.status_code}
    except ValidationError as e:
        logger.error(f"Validation error for symbol. Error: {e.json()}")
        return {"error": "Validation error", "details": e.errors(), "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY}
    except Exception as e:
        logger.error(f"Unhandled exception for forecast: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
