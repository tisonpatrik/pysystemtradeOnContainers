from sqlalchemy.orm import sessionmaker
from src.db.tables.business_data_tables.roll_calendars_table import RollCalendarsTable
import pandas as pd
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAPPING = {'CURRENT_CONTRACT': 'current_contract', 'NEXT_CONTRACT': 'next_contract', 'CARRY_CONTRACT':'carry_contract'}

def datetime_to_unix(dt_str):
    """Convert datetime string to unix timestamp (seconds since epoch)."""
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    return int(dt.timestamp())

def process_csv_file(filename, folder_path):
    """Read and process a single CSV file."""
    symbol = filename.split('.')[0]
    csv_file_path = os.path.join(folder_path, filename)
    
    logger.info(f"Seeding of {symbol} roll calendars started.")
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    df.rename(columns=MAPPING, inplace=True)
    
    # Convert the DATETIME column to UNIX_TIMESTAMP and drop the original column
    df['UNIX_TIMESTAMP'] = df['DATE_TIME'].apply(datetime_to_unix)
    df.drop(columns=['DATE_TIME'], inplace=True)
    
    # Add SYMBOL column
    df['SYMBOL'] = symbol
    
    return df.to_dict(orient='records')

async def seed_roll_calendars_table(async_session: sessionmaker):
    """Seed the roll calendars table from CSV files in the specified folder."""
    logger.info(f"Seeding of instrument roll calendars table started.")
    folder_path = "/path/in/container/multiple_prices_csv"

    # Iterate over all CSV files in the directory, process them, and insert into the database
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            data_for_file = process_csv_file(filename, folder_path)
            
            # Insert the processed data for the current file into the database
            async with async_session() as session:
                session.add_all([RollCalendarsTable(**data) for data in data_for_file])
                await session.commit()
                
            logger.info(f"Seeding of {filename} completed.")
    logger.info(f"Seeding of instrument roll calendars table finished.")
