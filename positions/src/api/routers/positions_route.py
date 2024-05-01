from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from common.src.logging.logger import AppLogger
from positions.src.api.models.portfolio_request_model import SubsystemPositionRequest

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.post(
    "/run_simulation/",
    status_code=status.HTTP_200_OK,
    name="run_simulation",
)
async def post_subsystem_position(request: SubsystemPositionRequest = Depends()):
    try:
        return request
    except HTTPException as e:
        logger.error(f"An error occurred while trying to run simulation. Error: {e.detail}")
        return {"error": e.detail, "status_code": e.status_code}
    except ValidationError as e:
        logger.error(f"Validation error for simulation. Error: {e.json()}")
        return {"error": "Validation error", "details": e.errors(), "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY}
