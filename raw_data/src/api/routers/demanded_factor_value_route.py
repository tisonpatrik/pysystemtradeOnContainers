from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_demanded_factor_value_query import GetDemandedFactorValueQuery
from common.src.logging.logger import AppLogger
from raw_data.src.api.dependencies.dependencies import get_demanded_factor_value_handler
from raw_data.src.api.handlers.demanded_factor_value_handler import DemandedFactorValueHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/demanded_factor_value/",
    status_code=status.HTTP_200_OK,
    name="Get demanded factor value",
)
async def get_demanded_factor_value_async(
    query: Annotated[GetDemandedFactorValueQuery, Query()],
    handler: DemandedFactorValueHandler = Depends(get_demanded_factor_value_handler),
):
    try:
        result = await handler.get_demanded_factor_value_async(query)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result
    except HTTPException as e:
        logger.exception("An error occurred while trying to get demanded factor value. Error: %s", e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for request. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception while processing request")
        raise HTTPException(status_code=500, detail="Internal server error") from None
