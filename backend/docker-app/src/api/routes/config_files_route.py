from fastapi import APIRouter, status
from src.handlers.config_data_handler import ConfigDataHandler
from src.handlers.database_handler import DatabaseHandler
from src.api.routes.utils import execute_with_logging

router = APIRouter()
config_handler = ConfigDataHandler()
db_handler = DatabaseHandler()

@router.post("/parse_files/", status_code=status.HTTP_200_OK, name="parse_files")
async def parse_files():
    """Parse files and store them in temp."""
    await execute_with_logging(config_handler.handle_data_processing, 
                               start_msg="File parsing started.",
                               end_msg="File parsing completed.")
    return {"status": "files were preprocessed and stored in the temp folder"}

@router.post("/seed_config_files/", status_code=status.HTTP_200_OK, name="seed_config_files")
async def fill_database():
    """Fill the database tables with data."""
    await execute_with_logging(db_handler.insert_data_from_csv,
                               start_msg="Database table filling started.",
                               end_msg="Database table filling completed.")
    return {"status": "Table was filled with data from temp folder"}
