from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.logging.logger import AppLogger
from rules.src.api.dependencies.dependencies import get_accel_handler
from rules.src.api.handlers.accel_handler import AccelHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_accel_route/",
    status_code=status.HTTP_200_OK,
    name="Get Accel",
)
async def get_accel_for_instrument_async(
    query: GetRuleForInstrumentQuery = Depends(),
    accel_handler: AccelHandler = Depends(get_accel_handler),
):
    try:
        accel = await accel_handler.get_accel_async(query)
        return accel.to_json(orient="records")
    except HTTPException as e:
        logger.error(f"An error occurred while trying to calculate accel for symbol {query.symbol}. Error: {e.detail}")
        return {"error": e.detail, "status_code": e.status_code}
    except ValidationError as e:
        logger.error(f"Validation error for symbol. Error: {e.json()}")
        return {"error": "Validation error", "details": e.errors(), "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY}
    except Exception as e:
        logger.error(f"Unhandled exception for symbol {query.symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")