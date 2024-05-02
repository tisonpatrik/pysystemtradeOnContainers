from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ValidationError

from common.src.logging.logger import AppLogger
from common.src.models.api_query_models import GetFxRateQuery
from risk.src.api.handlers.test_handler import TestHandler
from risk.src.dependencies.risk_dependencies import get_test_handler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_test_fx",
    status_code=status.HTTP_200_OK,
    name="get_test_fx",
)
async def get_test_fx(
    test_handler: TestHandler = Depends(get_test_handler),
    query: GetFxRateQuery = Depends(),
):
    try:
        instr_value_vol = await test_handler.get_test_fx(query)
        return instr_value_vol
    except HTTPException as e:
        logger.error(
            f"An error occurred while trying to fetch instrument volatility for symbol {query.symbol}. Error: {e.detail}"
        )
        return {"error": e.detail, "status_code": e.status_code}
    except ValidationError as e:
        logger.error(f"Validation error for symbol. Error: {e.json()}")
        return {"error": "Validation error", "details": e.errors(), "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY}
