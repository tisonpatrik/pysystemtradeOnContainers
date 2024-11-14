from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.rule_queries.get_normalized_momentum import GetNormalizedMomentumQuery
from common.src.logging.logger import AppLogger
from rules.api.dependencies.dependencies import get_normalized_momentum_handler
from rules.api.handlers.normalized_momentum_handler import NormalizedMomentumHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_normalized_momentum/",
    status_code=status.HTTP_200_OK,
    name="Get Normalized Momentum",
)
async def get_normalized_momentum_async(
    query: GetNormalizedMomentumQuery = Depends(),
    handler: NormalizedMomentumHandler = Depends(get_normalized_momentum_handler),
):
    try:
        result = await handler.get_normalized_momentum_async(query)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result
    except HTTPException as e:
        logger.exception("An error occurred while trying to calculate normalized momentum for symbol %s. Error: %s", query.symbol, e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
