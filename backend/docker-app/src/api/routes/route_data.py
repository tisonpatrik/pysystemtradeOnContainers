from fastapi import APIRouter, status
from src.handlers.data_handler import DataHandler
from src.handlers.database_handler import DatabaseHandler
import logging

router = APIRouter()

@router.post("/parse_files/", status_code=status.HTTP_200_OK, name="parse_files")
def parse_files():
    logging.info("File parsing started.")
    handler = DataHandler()
    handler.handle_data_processing()
    logging.info("File parsing completed.")
    return {"status": "files were preprocessed and stored in the temp folder"}

@router.post("/create_and_fill_db/", status_code=status.HTTP_200_OK, name="create_and_fill_db")
async def create_and_fill_db():
    logging.info("Database table creation and filling started.")
    
    handler = DatabaseHandler()
    await handler.insert_data_from_csv()
    
    logging.info("Database table creation and filling completed.")
    
    return {"status": "Table was created and filled with data from temp folder"}
