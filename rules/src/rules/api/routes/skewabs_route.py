from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_skew_rule_for_instrument import GetSkewRuleForInstrumentQuery
from common.src.logging.logger import AppLogger
from rules.api.dependencies.dependencies import get_skewabs_handler
from rules.api.handlers.skewabs_handler import SkewAbsHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_skewabs_route/",
    status_code=status.HTTP_200_OK,
    name="Get SkewAbs",
)
async def get_skewabs_async(
    query: GetSkewRuleForInstrumentQuery = Depends(),
    skewabs_handler: SkewAbsHandler = Depends(get_skewabs_handler),
):
    try:
        result = await skewabs_handler.get_skewabs_async(query.symbol, query.speed, lookback=query.lookback)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result
    except HTTPException as e:
        logger.exception("An error occurred while trying to calculate skewabs for symbol %s. Error: %s", query.symbol, e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
