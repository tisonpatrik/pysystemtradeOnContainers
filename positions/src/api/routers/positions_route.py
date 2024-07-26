from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.logging.logger import AppLogger
from positions.src.api.dependencies.positions_dependencies import get_positions_handler
from positions.src.api.handlers.positions_handler import PositionsHandler
from positions.src.api.models.positions_request_model import SubsystemPositionForInstrument

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.post(
    "/calculate_subsystem_position/",
    status_code=status.HTTP_200_OK,
    name="calculate_subsystem_position",
)
async def get_subsystem_position_for_instrument(
    request: SubsystemPositionForInstrument = Depends(),
    positions_handler: PositionsHandler = Depends(get_positions_handler),
):
    try:
        positions = await positions_handler.get_subsystem_position_async(request)
        return positions
    except HTTPException as e:
        logger.error(f"An error occurred while trying to run simulation. Error: {e.detail}")
        return {"error": e.detail, "status_code": e.status_code}
    except ValidationError as e:
        logger.error(f"Validation error for simulation. Error: {e.json()}")
        return {"error": "Validation error", "details": e.errors(), "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY}
