from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.logging.logger import AppLogger
from rules.src.api.dependencies.dependencies import get_cs_mean_reversion_handler
from rules.src.api.handlers.cs_mean_reversion_handler import CSMeanReversionHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_cs_mean_reversion_route/",
    status_code=status.HTTP_200_OK,
    name="Get Cross Sectional Mean Reversion",
)
async def get_cs_mean_reversion_async(
    query: GetRuleForInstrumentQuery = Depends(),
    momentum_handler: CSMeanReversionHandler = Depends(get_cs_mean_reversion_handler),
):
    try:
        result = await momentum_handler.get_cs_mean_reversion_async(query.symbol, query.speed)
        print(result)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result
    except HTTPException as e:
        logger.exception(
            "An error while trying to calculate Cross Sectional Mean Reversion for symbol %s. Error: %s", query.symbol, e.detail
        )
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
