from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.logging.logger import AppLogger
from forecast.src.api.dependencies.forecast_dependencies import get_raw_forecast_handler
from forecast.src.api.handlers.raw_forecast_handler import RawForecastHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_raw_forecast/",
    status_code=status.HTTP_200_OK,
    name="Get raw forecast",
)
async def get_instrument_currency_volalitlty_async(
    instrument_vol_handler: RawForecastHandler = Depends(get_raw_forecast_handler),
):
    try:
        raw_forecast = await instrument_vol_handler.get_raw_forecast_async()
        logger.info(f"Successfully fetched raw forecast: {raw_forecast}")
        return raw_forecast
    except HTTPException as e:
        logger.error(f"An error occurred while trying to fetch raw forecast. Error: {e.detail}")
        return {"error": e.detail, "status_code": e.status_code}
    except ValidationError as e:
        logger.error(f"Validation error for symbol. Error: {e.json()}")
        return {"error": "Validation error", "details": e.errors(), "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY}
    except Exception as e:
        logger.error(f"Unhandled exception for raw forecast: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
