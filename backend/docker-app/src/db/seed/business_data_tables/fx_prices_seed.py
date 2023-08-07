from sqlalchemy.orm import sessionmaker
from src.db.tables.fx_prices_table import FxPricesTable
import pandas as pd
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def datetime_to_unix(dt_str):
    # Convert datetime string to unix timestamp (seconds since epoch)
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    return int(dt.timestamp())

async def seed_fx_prices_table(async_session: sessionmaker):
    logger.info(f"Seeding of instrument fx prices table started.")
    folder_path = "/path/in/container/fx_prices_csv"
    async with async_session() as session:
        # Iterate over all CSV files in the directory
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                symbol = filename.split('.')[0]
                csv_file_path = os.path.join(folder_path, filename)
                
                # Read the CSV file into a DataFrame
                df = pd.read_csv(csv_file_path)
                
                # Convert the DATETIME column to UNIX_TIMESTAMP
                df['UNIX_TIMESTAMP'] = df['DATETIME'].apply(datetime_to_unix)
                df.drop(columns=['DATETIME'], inplace=True)
                
                # Add SYMBOL column
                df['SYMBOL'] = symbol
                
                # Iterate over rows and add to session
                for _, row in df.iterrows():
                    data = FxPricesTable(**row.to_dict())
                    session.add(data)
                
                # Commit the changes
                await session.commit()

    logger.info(f"Seeding of instrument fx prices table finished.")