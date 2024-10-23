from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_historic_average_factor_value_all_assets import GetHistoricAverageFactorValueAllAssetsQuery
from common.src.logging.logger import AppLogger
from raw_data.src.api.dependencies.dependencies import get_historic_average_factor_value_all_assets_handler
from raw_data.src.api.handlers.historic_average_factor_value_all_assets_handler import HistoricAverageFactorValueAllAssetsHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/historic_average_factor_value_all_assets/",
    status_code=status.HTTP_200_OK,
    name="Get historic average factor value for all assets",
)
async def get_historic_average_factor_value_all_assets_async(
    query: Annotated[GetHistoricAverageFactorValueAllAssetsQuery, Query()],
    handler: HistoricAverageFactorValueAllAssetsHandler = Depends(get_historic_average_factor_value_all_assets_handler),
):
    try:
        result = await handler.get_historic_avg_factor_value_for_all_assets_async(query)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result
    except HTTPException as e:
        logger.exception("An error occurred while trying to get historic average factor value for all assets. Error: %s", e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for request. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception while processing request")
        raise HTTPException(status_code=500, detail="Internal server error") from None
