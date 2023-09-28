"""
Module for handling raw data file routes.
This module provides an API endpoint for parsing raw data files and 
storing the preprocessed data in a temporary folder.
"""

from fastapi import APIRouter, status, Depends

from src.api.routes.utils import execute_with_logging_async
from src.handlers.raw_data_handler import RawDataHandler
from src.api.dependencies.repositories import get_repository

router = APIRouter()

@router.post("/parse_files/", status_code=status.HTTP_200_OK, name="parse_files")
async def parse_raw_data_files(raw_data_handler:RawDataHandler=Depends(get_repository(RawDataHandler))):
    """Parse raw data files and store them in temp."""
    await execute_with_logging_async(
        raw_data_handler.handle_data_processing,
        start_msg="Raw data file parsing started.",
        end_msg="Raw data file parsing completed.",
    )
    return {"status": "Raw data files were preprocessed and stored in the temp folder"}
