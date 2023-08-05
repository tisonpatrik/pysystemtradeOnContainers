from sqlalchemy import select, func
from sqlalchemy.future import Connection

from src.db.tables.multiple_prices_table import MultiplePricesTable
from src.db.seed.file_processing import get_all_csv_files_async, process_csv_file_async

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fill_empty_tables_async(session):
    # Check if tables are empty
    multiple_prices_empty = await check_table_empty_async(session)
    
    # If tables are empty, seed them
    if multiple_prices_empty:
        await seed_grayfox_db_async(session)
        
async def seed_grayfox_db_async(session):
    await seed_multiple_prices(session)

async def save_data_to_db_async(data, session):
    """Save processed data to the database using bulk insert."""
    
    records = data.to_dict(orient="records")
    instances = [MultiplePricesTable(**record) for record in records]
    
    session.add_all(instances)
    await session.commit()

    logger.info("Data has been successfully written to the database.")
   
async def seed_multiple_prices(session):
    directory_path = "/path/in/container" + "/multiple_prices_csv"
    logging.info("Seeding of multiple_prices table started.")
    logging.info("Checking files in the directory.")
    csv_files = await get_all_csv_files_async(directory_path)
    for file in csv_files:
        file_path = os.path.join(directory_path, file)
        data = await process_csv_file_async(file_path)
        await save_data_to_db_async(data, session)
    logging.info("Finished processing all files.")

async def check_tables_exist_async(conn: Connection):
    """Check if the MultiplePrices table exists."""
    try:
        # Try to fetch one row from the table to check its existence
        await conn.execute(select(MultiplePricesTable).limit(1))
        return True
    except Exception as e:
        logger.error(f"Error checking if table exists: {e}")
        return False
        
async def check_table_empty_async(session):
    count = await session.execute(select(func.count()).select_from(MultiplePricesTable))
    return count.scalar() == 0