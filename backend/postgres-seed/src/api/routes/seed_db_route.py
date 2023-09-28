"""
Module for handling the seeding of the database.
This module provides an API endpoint for filling the database tables with data 
from preprocessed files stored in the temporary folder.
"""

from fastapi import APIRouter, status, Depends

from src.api.routes.utils import execute_with_logging_async
from src.handlers.seed_db_handler import SeedDBHandler
from src.api.dependencies.repositories import get_repository

router = APIRouter()

@router.post("/seed_db/", status_code=status.HTTP_200_OK, name="seed_db")
async def fill_database(seed_db_handler:SeedDBHandler=Depends(get_repository(SeedDBHandler))):
    """Fill the database tables with data."""
    await execute_with_logging_async(
        seed_db_handler.insert_data_from_csv_async,
        start_msg="Database table filling started.",
        end_msg="Database table filling completed.",
    )
    return {"status": "Table was filled with data from temp folder"}
