from src.db.repositories.repository import PostgresRepository

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INSTRUMENTS_CONFIG_MAPPING = {'Instrument': 'symbol', 'Description': 'description', 'Pointsize': 'pointsize', 'Currency': 'currency', 'AssetClass': 'asset_class', 'PerBlock': 'per_block', 'Percentage': 'percentage', 'PerTrade': 'per_trade', 'Region': 'region'}
SQL_COMMAND = """
    CREATE TABLE instrument_config (
        SYMBOL VARCHAR(255) PRIMARY KEY, 
        DESCRIPTION TEXT, 
        POINTSIZE FLOAT, 
        CURRENCY VARCHAR(10), 
        ASSET_CLASS VARCHAR(50), 
        PER_BLOCK FLOAT, 
        PERCENTAGE FLOAT, 
        PER_TRADE INTEGER, 
        REGION VARCHAR(50)
    )
    """

async def seed_instrumnent_config_table_async():
    logger.info(f"Seeding of instrumnent config table started.")

    df = load_files()    
    await write_records_async(df)

    logger.info(f"Seeding of instrumnent config table finished.")

def load_files() -> pd.DataFrame:
    csv_file_path = "/path/in/container/csvconfig/instrumentconfig.csv"
    df = pd.read_csv(csv_file_path)
    df.rename(columns=INSTRUMENTS_CONFIG_MAPPING, inplace=True)
    return df

async def write_records_async(df: pd.DataFrame):
    repository= PostgresRepository()
    repository.create_table(sql_command=SQL_COMMAND)
    await repository.insert_data_async(df=df, table_name="instrument_config")