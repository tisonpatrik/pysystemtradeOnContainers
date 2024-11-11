from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_relative_skew_deviation import GetRelativeSkewDeviationQuery
from common.src.logging.logger import AppLogger
from raw_data.api.dependencies.dependencies import get_relative_skew_deviation_handler
from raw_data.api.handlers.relative_skew_deviation_handler import RelativeSkewDeviationHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_relative_skew_deviation/",
    status_code=status.HTTP_200_OK,
    name="Get relative skew deviation",
)
async def get_relative_skew_deviation(
    query: Annotated[GetRelativeSkewDeviationQuery, Query()],
    handler: RelativeSkewDeviationHandler = Depends(get_relative_skew_deviation_handler),
):
    try:
        result = await handler.get_relative_skew_deviation_async(query)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result
    except HTTPException as e:
        logger.exception("An error occurred while trying to get relative skew deviation. Error: %s", e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for request. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception while processing request")
        raise HTTPException(status_code=500, detail="Internal server error") from None
