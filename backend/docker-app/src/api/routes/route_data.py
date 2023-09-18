from fastapi import APIRouter, status
from src.handlers.config_data_handler import ConfigDataHandler
from src.handlers.database_handler import DatabaseHandler
from src.handlers.data_handler import DataHandler
from src.api.routes.utils import execute_with_logging

router = APIRouter()

config_handler = ConfigDataHandler()
data_handler = DataHandler()
db_handler = DatabaseHandler()

@router.post("/parse_timeseries_files/", status_code=status.HTTP_200_OK, name="parse_timeseries_files")
async def parse_timeseries_files():
    """Parse time series files and store them in temp."""
    await execute_with_logging(data_handler.handle_data_processing,
                               start_msg="Time series file parsing started.",
                               end_msg="Time series file parsing completed.")
    return {"status": "Time series files were preprocessed and stored in the temp folder"}

@router.post("/fill_timeseries_db/", status_code=status.HTTP_200_OK, name="fill_timeseries_db")
async def fill_timeseries_database():
    """Fill the database tables with time series data."""
    await execute_with_logging(data_handler.insert_data_from_csv,
                               start_msg="Database time series table filling started.",
                               end_msg="Database time series table filling completed.")
    return {"status": "Time series table was filled with data from temp folder"}


@router.post("/init_tables/", status_code=status.HTTP_200_OK, name="init_tables")
async def initialize_tables():
    """Initialize tables in the database."""
    await execute_with_logging(db_handler.init_tables,
                               start_msg="Init of tables has started.",
                               end_msg="Init of tables was completed.")
    return {"status": "tables of db were created"}

@router.post("/reset_db/", status_code=status.HTTP_200_OK, name="reset_db")
async def reset_database():
    """Reset the database tables."""
    await execute_with_logging(db_handler.reset_tables,
                               start_msg="Database table reset started.",
                               end_msg="Database table reset is complete.")
    return {"status": "Database was reset."}
