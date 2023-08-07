from sqlalchemy.orm import sessionmaker
from src.db.tables.multiple_prices_table import MultiplePricesTable
import pandas as pd
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def datetime_to_unix(dt_str):
    """Convert datetime string to unix timestamp (seconds since epoch)."""
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    return int(dt.timestamp())

def process_csv_file(filename, folder_path):
    """Read and process a single CSV file."""
    symbol = filename.split('.')[0]
    csv_file_path = os.path.join(folder_path, filename)
    
    logger.info(f"Seeding of {symbol} multiple prices started.")
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Convert the DATETIME column to UNIX_TIMESTAMP and drop the original column
    df['UNIX_TIMESTAMP'] = df['DATETIME'].apply(datetime_to_unix)
    df.drop(columns=['DATETIME'], inplace=True)
    
    # Add SYMBOL column
    df['SYMBOL'] = symbol
    
    return df.to_dict(orient='records')

async def seed_multiple_prices_table(async_session: sessionmaker):
    """Seed the multiple prices table from CSV files in the specified folder."""
    logger.info(f"Seeding of instrument multiple prices table started.")
    folder_path = "/path/in/container/multiple_prices_csv"
    all_data = []

    # Iterate over all CSV files in the directory and process them
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            all_data.extend(process_csv_file(filename, folder_path))

    # Insert all records into the database in bulk
    async with async_session() as session:
        session.add_all([MultiplePricesTable(**data) for data in all_data])
        await session.commit()

    logger.info(f"Seeding of instrument multiple prices table finished.")
