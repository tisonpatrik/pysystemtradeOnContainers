from sqlalchemy import select, func
from sqlalchemy.future import Connection

from src.db.tables.multiple_prices_table import MultiplePricesTable
from src.db.tables.adjusted_prices_table import AdjustedPricesTable
from src.db.tables.fx_prices_table import FxPricesTable
from src.db.tables.roll_calendars_table import RollCalendarsTable
from src.db.tables.instrument_config_table import InstrumentConfigTable
from src.db.tables.instrument_metadata_table import InstrumentMetadataTable
from src.db.tables.roll_config_table import RollConfigTable
from src.db.tables.spread_costs_table import SpreadCostTable

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
INSTRUMENTS_CONFIG_MAPPING = {'SYMBOL': 'Instrument','DESCRIPTION': 'Description', 'POINTSIZE': 'Pointsize', 'CURRENCY': 'Currency', 'ASSET_CLASS': 'AssetClass', 'PER_BLOCK': 'PerBlock', 'PERCENTAGE': 'Percentage', 'PER_TRADE': 'PerTrade', 'REGION': 'Region'}
INSTRUMENT_METADATA_MAPPING = {'SYMBOL': 'Instrument','ASSET_CLASS': 'AssetClass', 'SUB_CLASS': 'SubClass', 'SUB_SUB_CLASS': 'SubSubClass', 'STYLE': 'Style', 'COUNTRY': 'Country', 'DURATION': 'Duration', 'DESCRIPTION': 'Description'}
ROLL_CONFIG_MAPPING = {'SYMBOL': 'Instrument', 'HOLD_ROLL_CYCLE': 'HoldRollCycle', 'ROLL_OFFSET_DAYS': 'RollOffsetDays', 'CARRY_OFFSET': 'CarryOffset', 'PRICED_ROLL_CYCLE': 'PricedRollCycle', 'EXPIRY_OFFSET': 'ExpiryOffset'}
SPREAD_COST_MAPPING = {'SYMBOL': 'Instrument','SPREAD_COST': 'SpreadCost'}

# Configuration for tables and their corresponding directories
TABLES_TO_SEED = [
    {"model": MultiplePricesTable, "directory": "/path/in/container/multiple_prices_csv", "mapping": MULTIPLE_PRICES_MAPPING},
    {"model": AdjustedPricesTable, "directory": "/path/in/container/adjusted_prices_csv", "mapping": ADJUSTED_PRICES_MAPPING},
    {"model": FxPricesTable, "directory": "/path/in/container/fx_prices_csv", "mapping": FX_PRICES_MAPPING},
    {"model": RollCalendarsTable, "directory": "/path/in/container/roll_calendars_csv", "mapping": ROLL_CALENDAR_MAPPING}
]
CONFIG_TO_SEED = [
    {"model": InstrumentConfigTable, "directory": "/path/in/container/instrumentconfig.csv", "mapping": MULTIPLE_PRICES_MAPPING},
    {"model": InstrumentMetadataTable, "directory": "/path/in/container/moreinstrumentinfo.csv", "mapping": ADJUSTED_PRICES_MAPPING},
    {"model": RollConfigTable, "directory": "/path/in/container/rollconfig.csv", "mapping": FX_PRICES_MAPPING},
    {"model": SpreadCostTable, "directory": "/path/in/container/spreadcosts.csv", "mapping": ROLL_CALENDAR_MAPPING}
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

async def seed_config_tables_async(session, table_model, file_path: str, column_mapping: dict):
    logger.info(f"Seeding of {table_model.__name__} table started.")
    logger.info("Checking file.")
    
    # Check if the file exists
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return

    # Assuming file name represents a symbol for transformation (this is based on the seed_table_async method)
    symbol = os.path.basename(file_path).split(".")[0]
    
    # Transform CSV data to match table's schema
    data = transform_csv_to_schema_general(file_path, symbol, column_mapping)
    
    # Check if data is not None and not empty before proceeding
    if data is not None and not data.empty:
        records = data.to_dict(orient="records")
        
        # Create instances of the table's model with the transformed data
        instances = [table_model(**record) for record in records]
        
        # Add the instances to the session for database insertion
        session.add_all(instances)
        
        # Commit the session to save changes to the database
        await session.commit()
    
    logger.info(f"Finished processing files for {table_model.__name__} table.")

async def fill_empty_tables_config_based_async(session):
    for config_table in CONFIG_TO_SEED:
        table_empty = await is_table_empty_async(session, config_table["model"])
        if table_empty:
            await seed_config_tables_async(session, config_table["model"], config_table["file"], config_table["mapping"])

    for data_table in TABLES_TO_SEED:
        table_empty = await is_table_empty_async(session, data_table["model"])
        if table_empty:
            await seed_table_async(session, data_table["model"], data_table["directory"], data_table["mapping"])

async def check_tables_exist_async(conn: Connection, table_model):
    """Check if a given table exists."""
    try:
        await conn.execute(select(table_model).limit(1))
        return True
    except Exception as e:
        logger.error(f"Error checking if table exists: {e}")
        return False