from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.cqrs.api_queries.rule_queries.get_skewrel import GetSkewRelQuery
from common.logging.logger import AppLogger
from rules.api.dependencies.dependencies import get_skewrel_handler
from rules.api.handlers.skewrel_handler import SkewRelHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_skewrel/",
    status_code=status.HTTP_200_OK,
    name="Get SkewRel",
)
async def get_skewrel_async(
    query: GetSkewRelQuery = Depends(),
    skewrel_handler: SkewRelHandler = Depends(get_skewrel_handler),
):
    try:
        result = await skewrel_handler.get_skewrel_async(query)
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
