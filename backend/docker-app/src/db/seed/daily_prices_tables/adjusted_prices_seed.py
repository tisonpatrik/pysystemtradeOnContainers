from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from src.db.tables.business_data_tables.raw_adjusted_prices_table import RawAdjustedPricesTable
from src.db.tables.daily_prices.adjusted_prices_table import AdjustedPricesTable
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_daily_adjusted_prices_table(async_session: sessionmaker):
    logger.info(f"Seeding of daily adjusted prices table started.")

    # Fetch all data from RawMultiplePricesTable
    async with async_session() as session:
        result = await session.execute(select(RawAdjustedPricesTable))
        raw_prices_data = result.scalars().all()

    # Convert the data to a DataFrame for easy resampling
    df = pd.DataFrame([data.__dict__ for data in raw_prices_data])
    df['date'] = pd.to_datetime(df['UNIX_TIMESTAMP'], unit='s')  # Convert UNIX_TIMESTAMP to datetime
    df.set_index('date', inplace=True)

    # Resample to daily data (taking the last entry for each day)
    daily_data = df.resample('D').mean().dropna()

    # Insert resampled data into MultiplePricesTable
    async with async_session() as session:
                session.add_all([AdjustedPricesTable(**data) for data in daily_data])
                await session.commit()

    logger.info(f"Seeding of daily adjusted prices table finished.")
