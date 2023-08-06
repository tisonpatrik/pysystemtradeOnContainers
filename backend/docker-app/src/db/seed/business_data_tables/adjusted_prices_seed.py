from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.tables.adjusted_prices_table import AdjustedPricesTable
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

async def seed_instrumnent_config_table(session: AsyncSession):
    logger.info(f"Seeding of instrument adjusted prices table started.")
    folder_path = "/path/in/container/adjusted_prices_csv"

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
                adjusted_price = AdjustedPricesTable(**row.to_dict())
                session.add(adjusted_price)
            
            # Commit the changes
            await session.commit()

    logger.info(f"Seeding of instrument adjusted prices table finished.")