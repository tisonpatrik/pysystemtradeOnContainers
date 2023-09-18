from fastapi import APIRouter, status, HTTPException
from src.handlers.config_data_handler import ConfigDataHandler
from src.handlers.database_handler import DatabaseHandler
import logging

router = APIRouter()

config_handler = ConfigDataHandler()
db_handler = DatabaseHandler()

async def execute_with_logging(task, *args, start_msg, end_msg):
    """Helper function to wrap task execution with logging."""
    logging.info(start_msg)
    
    try:
        await task(*args)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while processing the request.")
    
    logging.info(end_msg)


@router.post("/parse_files/", status_code=status.HTTP_200_OK, name="parse_files")
async def parse_files():
    """Parse files and store them in temp."""
    await execute_with_logging(config_handler.handle_data_processing, 
                               start_msg="File parsing started.",
                               end_msg="File parsing completed.")
    return {"status": "files were preprocessed and stored in the temp folder"}


@router.post("/init_tables/", status_code=status.HTTP_200_OK, name="init_tables")
async def initialize_tables():
    """Initialize tables in the database."""
    await execute_with_logging(db_handler.init_tables,
                               start_msg="Init of tables has started.",
                               end_msg="Init of tables was completed.")
    return {"status": "tables of db were created"}


@router.post("/fill_db/", status_code=status.HTTP_200_OK, name="fill_db")
async def fill_database():
    """Fill the database tables with data."""
    await execute_with_logging(db_handler.insert_data_from_csv,
                               start_msg="Database table filling started.",
                               end_msg="Database table filling completed.")
    return {"status": "Table was filled with data from temp folder"}


@router.post("/reset_db/", status_code=status.HTTP_200_OK, name="reset_db")
async def reset_database():
    """Reset the database tables."""
    await execute_with_logging(db_handler.reset_tables,
                               start_msg="Database table reset started.",
                               end_msg="Database table reset is complete.")
    return {"status": "Database was reset."}
