"""
Module for handling config file routes.
This module provides API endpoints related to config file operations such as parsing 
and preprocessing the files before storing them in the temp folder.
"""

from fastapi import APIRouter, status, Depends

from src.api.routes.utils import execute_with_logging
from src.handlers.config_data_handler import ConfigDataHandler
from src.api.dependencies.repositories import get_repository

router = APIRouter()

@router.post("/parse_files/", status_code=status.HTTP_200_OK, name="parse_files")
def parse_files(config_handler: ConfigDataHandler = Depends(get_repository(ConfigDataHandler))):
    """Parse files and store them in temp."""
    execute_with_logging(
        config_handler.handle_data_processing,
        start_msg="File parsing started.",
        end_msg="File parsing completed.",
    )
    return {"status": "files were preprocessed and stored in the temp folder"}
