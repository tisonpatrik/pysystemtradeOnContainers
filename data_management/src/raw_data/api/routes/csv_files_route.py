"""
API module for counting CSV files in specified directories.
Exposes a FastAPI endpoint that utilizes the CsvFilesHandler class for the counting operation.
"""

import logging

from fastapi import APIRouter, HTTPException, status

from src.raw_data.api.handlers.csv_files_handler import CsvFilesHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter()

@router.get(
    "/get_csv_file_counts/",
    status_code=status.HTTP_200_OK,
    name="Get Count of Mounted CSV Files",
)
async def get_csv_file_counts():
    """
    Returns the count of CSV files in specified directories.
    """
    try:
        seed_db_handler = CsvFilesHandler()
        counts = await seed_db_handler.get_count_of_mounted_files_async()

        logger.info("Successfully counted CSV files: %s", counts)
        return {
            "status": "success",
            "message": "Successfully counted CSV files.",
            "counts": counts,
        }

    except Exception as error:
        logger.error("Failed to count CSV files: %s", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while counting CSV files.",
        ) from error
