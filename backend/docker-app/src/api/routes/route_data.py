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

@router.post("/init_tables/", status_code=status.HTTP_200_OK, name="init_tables")
def parse_files():
    logging.info("Init of tables has started.")
    handler = DatabaseHandler()
    handler.init_tables()
    logging.info("Init of tables was completed.")
    return {"status": "tables of db was created"}

@router.post("/fill_db/", status_code=status.HTTP_200_OK, name="fill_db")
async def create_and_fill_db():
    logging.info("Database table filling started.")
    
    handler = DatabaseHandler()
    await handler.insert_data_from_csv()
    
    logging.info("Database table filling completed.")
    
    return {"status": "Table was filled with data from temp folder"}

@router.post("/reset_db/", status_code=status.HTTP_200_OK, name="reset_db")
def create_and_fill_db():
    logging.info("Database table filling started.")
    
    handler = DatabaseHandler()
    handler.reset_tables()
    
    logging.info("Database table reset is complete.")
    
    return {"status": "Database was reseted."}
