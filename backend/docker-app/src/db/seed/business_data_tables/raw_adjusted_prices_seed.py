from sqlalchemy.orm import sessionmaker
from src.db.tables.business_data_tables.raw_adjusted_prices_table import RawAdjustedPricesTable
import pandas as pd
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COLUMN_MAPPING = {'price': 'PRICE'}

def datetime_to_unix(dt_str):
    """Convert datetime string to unix timestamp (seconds since epoch)."""
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    return int(dt.timestamp())

def process_csv_file(filename, folder_path):
    """Read and process a single CSV file."""
    symbol = filename.split('.')[0]
    csv_file_path = os.path.join(folder_path, filename)
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    df.rename(columns=COLUMN_MAPPING, inplace=True)
    
    # Convert the DATETIME column to UNIX_TIMESTAMP and drop the original column
    df['UNIX_TIMESTAMP'] = df['DATETIME'].apply(datetime_to_unix)
    df.drop(columns=['DATETIME'], inplace=True)
    
    # Add SYMBOL column
    df['SYMBOL'] = symbol
    
    # Drop duplicates based on 'UNIX_TIMESTAMP' and 'SYMBOL'
    df.drop_duplicates(subset=['UNIX_TIMESTAMP', 'SYMBOL'], inplace=True)
    
    return df.to_dict(orient='records')

async def seed_raw_adjusted_prices_table(async_session: sessionmaker):
    """Seed the adjusted prices table from CSV files in the specified folder."""
    logger.info(f"Seeding of instrument adjusted prices table started.")
    folder_path = "/path/in/container/adjusted_prices_csv"

    # Iterate over all CSV files in the directory, process them, and insert into the database
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            data_for_file = process_csv_file(filename, folder_path)
            
            # Insert the processed data for the current file into the database
            async with async_session() as session:
                session.add_all([RawAdjustedPricesTable(**data) for data in data_for_file])
                await session.commit()
                
            logger.info(f"Seeding of {filename} completed.")

    logger.info(f"Seeding of instrument adjusted prices table finished.")
