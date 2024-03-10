from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.handlers.test_handler import TestHandler

from common.src.database.dependencies import get_db
from common.src.logging.logger import AppLogger

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/get_count_of_instrument_config_items/",
    status_code=status.HTTP_201_CREATED,
    name="Get count of config data items",
)
async def get_instrument_config_items_count_async(
    db_session: AsyncSession = Depends(get_db),
):
    """
    Asynchronously retrieves the count of instrument configuration items from the database.
    """
    try:
        config_items_handler = TestHandler(db_session)
        count = await config_items_handler.get_config_items_count_async()

        logger.info(
            f"Successfully retrieved count of instrument configuration items: {count}"
        )
        return {
            "status": "success",
            "message": f"Successfully retrieved count of instrument configuration items: {count}",
        }

    except Exception as error:
        logger.error(
            f"Failed to retrieve instrument configuration items count: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the instrument configuration items count from the database.",
        ) from error
