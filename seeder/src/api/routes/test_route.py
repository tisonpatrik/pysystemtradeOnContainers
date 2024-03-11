from fastapi import APIRouter, Depends, HTTPException, status
from httpx import AsyncClient

from common.src.database.dependencies import get_db
from common.src.logging.logger import AppLogger

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


@router.get(
    "/test_route/",
    status_code=status.HTTP_200_OK,
)
async def get_instrument_config_count():
    """
    Retrieves the count of instrument config items.
    """
    try:
        async with AsyncClient() as client:
            response = await client.get(
                "http://localhost:8000/test_router/get_count_of_instrument_config_items/"
            )
            if response.status_code == 200:
                count = response.json()["count"]
                logger.info(
                    f"Successfully retrieved count of instrument config items: {count}"
                )
                return {
                    "status": "success",
                    "count": count,
                }
            else:
                logger.error(
                    f"Failed to retrieve count, status code: {response.status_code}"
                )
                return {
                    "status": "error",
                    "message": "Failed to retrieve count of instrument config items.",
                }

    except Exception as error:
        logger.error(
            "Failed to retrieve count of instrument config items: %s", str(error)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving count of instrument config items.",
        ) from error
