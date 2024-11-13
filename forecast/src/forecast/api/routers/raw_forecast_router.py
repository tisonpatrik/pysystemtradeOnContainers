from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_forecast_for_symbol_query import GetForecastForSymbolQuery
from common.src.logging.logger import AppLogger
from forecast.api.dependencies.dependencies import get_combined_forecast_handler
from forecast.api.handlers.combined_forecast_handler import CombineForecastHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_combined_forecast/",
    status_code=status.HTTP_200_OK,
    name="Get combine forecast",
)
async def get_combined_forecast(
    query: GetForecastForSymbolQuery = Depends(),
    combined_forecast_handler: CombineForecastHandler = Depends(get_combined_forecast_handler),
):
    try:
        result = await combined_forecast_handler.get_combined_forecast_async(query.symbol)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result

    except HTTPException as e:
        logger.exception("An error occurred while trying to get combine forecast for symbol %s. Error: %s", query.symbol, e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
