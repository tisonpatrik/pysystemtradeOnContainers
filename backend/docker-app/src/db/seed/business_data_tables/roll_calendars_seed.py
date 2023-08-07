from sqlalchemy.orm import sessionmaker
from src.db.tables.roll_calendars_table import RollCalendarsTable
import pandas as pd
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAPPING = {'CURRENT_CONTRACT': 'current_contract', 'NEXT_CONTRACT': 'next_contract', 'CARRY_CONTRACT':'carry_contract'}


def datetime_to_unix(dt_str):
    # Convert datetime string to unix timestamp (seconds since epoch)
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    return int(dt.timestamp())

async def seed_roll_calendars_table(async_session: sessionmaker):
    logger.info(f"Seeding of instrument roll calendars table started.")
    folder_path = "/path/in/container/multiple_prices_csv"
    async with async_session() as session:
        # Iterate over all CSV files in the directory
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                symbol = filename.split('.')[0]
                csv_file_path = os.path.join(folder_path, filename)
                
                # Read the CSV file into a DataFrame
                df = pd.read_csv(csv_file_path)
                df.rename(columns=MAPPING, inplace=True)
                # Convert the DATETIME column to UNIX_TIMESTAMP
                df['UNIX_TIMESTAMP'] = df['DATE_TIME'].apply(datetime_to_unix)
                df.drop(columns=['DATE_TIME'], inplace=True)
                
                # Add SYMBOL column
                df['SYMBOL'] = symbol
                
                # Iterate over rows and add to session
                for _, row in df.iterrows():
                    data = RollCalendarsTable(**row.to_dict())
                    session.add(data)
                
                # Commit the changes
                await session.commit()

    logger.info(f"Seeding of instrument roll calendars table finished.")