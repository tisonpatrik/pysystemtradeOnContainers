from sqlalchemy import select, func
from sqlalchemy.future import Connection

from src.db.tables.multiple_prices_table import MultiplePricesTable
from src.db.seed.file_processing import get_all_csv_files_async, process_csv_file_async

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration for tables and their corresponding directories
TABLES_TO_SEED = [
    {"model": MultiplePricesTable, "directory": "/path/in/container/multiple_prices_csv"}
    # Add more tables as needed
]

async def is_table_empty_async(session, table_model):
    count = await session.execute(select(func.count()).select_from(table_model))
    return count.scalar() == 0

async def seed_table_async(session, table_model, directory_path: str):
    logger.info(f"Seeding of {table_model.__name__} table started.")
    logger.info("Checking files in the directory.")
    
    csv_files = await get_all_csv_files_async(directory_path)
    for file in csv_files:
        file_path = os.path.join(directory_path, file)
        data = await process_csv_file_async(file_path)
        records = data.to_dict(orient="records")
        instances = [table_model(**record) for record in records]
        session.add_all(instances)
        await session.commit()
    
    logger.info(f"Finished processing files for {table_model.__name__} table.")

async def fill_empty_tables_config_based_async(session):
    for table_config in TABLES_TO_SEED:
        table_empty = await is_table_empty_async(session, table_config["model"])
        if table_empty:
            await seed_table_async(session, table_config["model"], table_config["directory"])

async def check_tables_exist_async(conn: Connection, table_model):
    """Check if a given table exists."""
    try:
        # Try to fetch one row from the table to check its existence
        await conn.execute(select(table_model).limit(1))
        return True
    except Exception as e:
        logger.error(f"Error checking if table exists: {e}")
        return False