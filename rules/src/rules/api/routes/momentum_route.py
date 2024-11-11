from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.logging.logger import AppLogger
from rules.api.dependencies.dependencies import get_momentum_handler
from rules.api.handlers.momentum_handler import MomentumHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_momentum_route/",
    status_code=status.HTTP_200_OK,
    name="Get Momentum",
)
async def get_momentum_async(
    query: GetRuleForInstrumentQuery = Depends(),
    momentum_handler: MomentumHandler = Depends(get_momentum_handler),
):
    try:
        result = await momentum_handler.get_momentum_async(query.symbol, query.speed)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result
    except HTTPException as e:
        logger.exception("An error while trying to calculate momentum for symbol %s. Error: %s", query.symbol, e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
