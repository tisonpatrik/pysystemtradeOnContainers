from sqlalchemy import select, func
from sqlalchemy.future import Connection

from src.db.tables.multiple_prices_table import MultiplePricesTable
from src.db.tables.adjusted_prices_table import AdjustedPricesTable
from src.db.tables.fx_prices_table import FxPricesTable
from src.db.tables.roll_calendars_table import RollCalendarsTable
from src.db.seed.file_processing import get_all_csv_files_async, transform_csv_to_schema_general

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Column mappings for each table
MULTIPLE_PRICES_MAPPING = {'CARRY': 'CARRY', 'CARRY_CONTRACT': 'CARRY_CONTRACT', 'PRICE': 'PRICE', 'PRICE_CONTRACT': 'PRICE_CONTRACT', 'FORWARD': 'FORWARD', 'FORWARD_CONTRACT': 'FORWARD_CONTRACT'}
ADJUSTED_PRICES_MAPPING = {'PRICE': 'price'}
FX_PRICES_MAPPING = {'PRICE': 'PRICE'}
ROLL_CALENDAR_MAPPING = {'CURRENT_CONTRACT': 'current_contract', 'NEXT_CONTRACT': 'next_contract', 'CARRY_CONTRACT':'carry_contract'}
# TODO: Define mappings for other tables here...

# Configuration for tables and their corresponding directories
TABLES_TO_SEED = [
    {"model": MultiplePricesTable, "directory": "/path/in/container/multiple_prices_csv", "mapping": MULTIPLE_PRICES_MAPPING},
    {"model": AdjustedPricesTable, "directory": "/path/in/container/adjusted_prices_csv", "mapping": ADJUSTED_PRICES_MAPPING},
    {"model": FxPricesTable, "directory": "/path/in/container/fx_prices_csv", "mapping": FX_PRICES_MAPPING},
    {"model": RollCalendarsTable, "directory": "/path/in/container/roll_calendars_csv", "mapping": ROLL_CALENDAR_MAPPING}
]
CONFIG_TO_SEED = [
    {"model": MultiplePricesTable, "directory": "/path/in/container/multiple_prices_csv", "mapping": MULTIPLE_PRICES_MAPPING},
    {"model": AdjustedPricesTable, "directory": "/path/in/container/adjusted_prices_csv", "mapping": ADJUSTED_PRICES_MAPPING},
    {"model": FxPricesTable, "directory": "/path/in/container/fx_prices_csv", "mapping": FX_PRICES_MAPPING},
    {"model": RollCalendarsTable, "directory": "/path/in/container/roll_calendars_csv", "mapping": ROLL_CALENDAR_MAPPING}
]

async def is_table_empty_async(session, table_model):
    count = await session.execute(select(func.count()).select_from(table_model))
    return count.scalar() == 0

async def seed_table_async(session, table_model, directory_path: str, column_mapping: dict):
    logger.info(f"Seeding of {table_model.__name__} table started.")
    logger.info("Checking files in the directory.")
    
    csv_files = await get_all_csv_files_async(directory_path)
    for file in csv_files:
        file_path = os.path.join(directory_path, file)
        symbol = os.path.basename(file_path).split(".")[0]
        data = transform_csv_to_schema_general(file_path, symbol, column_mapping)
        if data is not None and not data.empty:
            records = data.to_dict(orient="records")
            instances = [table_model(**record) for record in records]
            session.add_all(instances)
            await session.commit()
    
    logger.info(f"Finished processing files for {table_model.__name__} table.")

async def fill_empty_tables_config_based_async(session):
    for table_config in TABLES_TO_SEED:
        table_empty = await is_table_empty_async(session, table_config["model"])
        if table_empty:
            await seed_table_async(session, table_config["model"], table_config["directory"], table_config["mapping"])

async def check_tables_exist_async(conn: Connection, table_model):
    """Check if a given table exists."""
    try:
        await conn.execute(select(table_model).limit(1))
        return True
    except Exception as e:
        logger.error(f"Error checking if table exists: {e}")
        return False