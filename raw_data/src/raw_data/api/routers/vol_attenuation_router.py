from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.raw_data_queries.get_vol_attenuation import GetVolAttenuationQuery
from common.src.logging.logger import AppLogger
from raw_data.api.dependencies.dependencies import get_vol_attenuation_handler
from raw_data.api.handlers.vol_attenuation_handler import VolAttenuationHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_vol_attenuation/",
    status_code=status.HTTP_200_OK,
    name="Get volatility attenuation",
)
async def get_vol_attenuation_async(
    query: GetVolAttenuationQuery = Depends(),
    handler: VolAttenuationHandler = Depends(get_vol_attenuation_handler),
):
    try:
        result = await handler.get_vol_attenuation_async(query.symbol)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result
    except ValidationError as e:
        logger.exception("Validation error for symbol %s. Error: %s", query.symbol, e.errors())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", query.symbol)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from None
