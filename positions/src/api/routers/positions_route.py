from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.cqrs.api_queries.get_subsystem_positions import GetSubsystemPositionForInstrument
from common.src.logging.logger import AppLogger
from positions.src.api.dependencies.positions_dependencies import get_positions_handler
from positions.src.api.handlers.positions_handler import PositionsHandler

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.post(
    "/calculate_subsystem_position/",
    status_code=status.HTTP_200_OK,
    name="Calculate subsystem position",
)
async def get_subsystem_position_for_instrument(
    request: GetSubsystemPositionForInstrument = Depends(),
    positions_handler: PositionsHandler = Depends(get_positions_handler),
):
    try:
        result = await positions_handler.get_subsystem_position_async(request)
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for the given parameters")
        return result

    except HTTPException as e:
        logger.exception("An error occurred while trying to get subsystem position for symbol %s. Error: %s", request.symbol, e.detail)
        raise
    except ValidationError as e:
        logger.exception("Validation error for symbol. Error: %s", e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation error") from None
    except Exception:
        logger.exception("Unhandled exception for symbol %s", request.symbol)
        raise HTTPException(status_code=500, detail="Internal server error") from None
