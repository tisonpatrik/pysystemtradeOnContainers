from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_fx_prices import GetFxPricesQuery
from common.src.logging.logger import AppLogger
from raw_data.api.dependencies.dependencies import get_fx_prices_handler
from raw_data.api.handlers.fx_prices_handler import FxPricesHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_fx_rate_by_symbol/",
    status_code=status.HTTP_200_OK,
    name="Get Fx prices for symbol",
)
async def get_fx_rate_for_instrument(
    query: GetFxPricesQuery = Depends(),
    handler: FxPricesHandler = Depends(get_fx_prices_handler),
):
    try:
        result = await handler.get_fx_prices_for_symbol_async(query)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result

    except HTTPException as e:
        logger.exception("An error occurred while trying to get Fx prices for symbol %s. Error: %s", query.symbol, e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
