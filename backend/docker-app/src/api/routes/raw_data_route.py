from fastapi import APIRouter, status
from src.handlers.raw_data_handler import RawDataHandler
from src.api.routes.utils import execute_with_logging

router = APIRouter()

data_handler = RawDataHandler()

@router.post("/parse_raw_data_files/", status_code=status.HTTP_200_OK, name="parse_raw_data_files")
async def parse_raw_data_files():
    """Parse raw data files and store them in temp."""
    await execute_with_logging(data_handler.handle_data_processing,
                               start_msg="Raw data file parsing started.",
                               end_msg="Raw data file parsing completed.")
    return {"status": "Raw data files were preprocessed and stored in the temp folder"}

@router.post("/seed_raw_data/", status_code=status.HTTP_200_OK, name="seed_raw_data")
async def seed_raw_data():
    """Fill the database tables with raw data."""
    await execute_with_logging(data_handler.insert_data_from_csv,
                               start_msg="Database raw data table filling started.",
                               end_msg="Database raw data table filling completed.")
    return {"status": "Raw data table was filled with data from temp folder"}
