"""
Module for handling database related routes.
This module provides API endpoints for operations on the database such as 
initializing tables and resetting the database.
"""

from fastapi import APIRouter, status, Depends

from src.api.routes.utils import execute_with_logging_async
from src.handlers.database_handler import DatabaseHandler
from src.api.dependencies.repositories import get_repository

router = APIRouter()

@router.post("/init_tables/", status_code=status.HTTP_200_OK, name="init_tables")
async def initialize_tables(db_handler: DatabaseHandler = Depends(get_repository(DatabaseHandler))):
    """Initialize tables in the database."""
    await execute_with_logging_async(
        db_handler.init_tables_async,
        start_msg="Init of tables has started.",
        end_msg="Init of tables was completed.",
    )
    return {"status": "tables of db were created"}

@router.post("/reset_db/", status_code=status.HTTP_200_OK, name="reset_db")
async def reset_database(db_handler: DatabaseHandler = Depends(get_repository(DatabaseHandler))):
    """Reset the database tables."""
    await execute_with_logging_async(
        db_handler.reset_tables_async,
        start_msg="Database table reset started.",
        end_msg="Database table reset is complete.",
    )
    return {"status": "Database was reset."}
