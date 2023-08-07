from sqlalchemy.orm import sessionmaker
from src.db.tables.business_data_tables.raw_multiple_prices_table import RawMultiplePricesTable
from src.db.tables.daily_prices.multiple_prices_table import MultiplePricesTable
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_daily_multiple_prices_table(async_session: sessionmaker):
    logger.info(f"Seeding of daily multiple prices table started.")

    # Fetch all data from RawMultiplePricesTable
    async with async_session() as session:
        raw_prices_data = await session.query(RawMultiplePricesTable).all()

    # Convert the data to a DataFrame for easy resampling
    df = pd.DataFrame([data.__dict__ for data in raw_prices_data])
    df['date'] = pd.to_datetime(df['UNIX_TIMESTAMP'], unit='s')  # Convert UNIX_TIMESTAMP to datetime
    df.set_index('date', inplace=True)

    # Resample to daily data (taking the last entry for each day)
    daily_data = df.resample('D').last().dropna()

    # Insert resampled data into MultiplePricesTable
    async with async_session() as session:
                session.add_all([MultiplePricesTable(**data) for data in daily_data])
                await session.commit()

    logger.info(f"Seeding of daily multiple prices table finished.")

