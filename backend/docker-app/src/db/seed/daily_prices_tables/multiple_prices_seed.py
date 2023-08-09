from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from src.db.tables.business_data_tables.raw_multiple_prices_table import RawMultiplePricesTable
from src.db.tables.daily_prices.multiple_prices_table import MultiplePricesTable
from src.db.tables.config_tables.instrument_config_table import InstrumentConfigTable
import pandas as pd
from pandas import DataFrame
import logging
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_all_symbols(async_session: sessionmaker) -> List[str]:
    """Retrieve all symbols from the instrument_config table."""
    try:
        async with async_session() as session:
            symbols_query = select(InstrumentConfigTable.SYMBOL)
            symbols_result = await session.execute(symbols_query)
            return [row.SYMBOL for row in symbols_result]
    except Exception as e:
        logger.error(f"Error fetching symbols: {e}")
        raise

async def fetch_prices_for_symbol(async_session: sessionmaker, symbol: str) -> DataFrame:
    """Fetch all prices for a given symbol from the raw_adjusted_prices table."""
    try:
        async with async_session() as session:
            prices_query = select(RawMultiplePricesTable).where(RawMultiplePricesTable.SYMBOL == symbol).order_by(RawMultiplePricesTable.UNIX_TIMESTAMP)
            prices_result = await session.execute(prices_query)
            
            # Transforming the result into a list of dictionaries for DataFrame conversion
            data = [dict(row) for row in prices_result]
            
            return DataFrame(data)
    except Exception as e:
        logger.error(f"Error fetching prices for instrument {symbol}: {e}")
        raise


def transform_prices_to_daily(df: DataFrame) -> DataFrame:
    """Convert UNIX_TIMESTAMP to datetime, set it as index, and resample to daily mean."""
    try:
        df['DATETIME'] = pd.to_datetime(df['UNIX_TIMESTAMP'], unit='s')
        df.set_index('DATETIME', inplace=True)
        return df[['PRICE']].resample('D').mean().dropna()
    except Exception as e:
        logger.error(f"Error transforming prices to daily format: {e}")
        raise

async def seed_daily_multiple_prices_table(async_session: sessionmaker) -> None:
    """Main function to seed the daily adjusted prices table."""
    logger.info(f"Seeding of daily adjusted prices table started.")
    
    try:
        symbols = await get_all_symbols(async_session)
        for symbol in symbols:
            logger.info(f"Processing instrument: {symbol} of adjusted prices table")
            df = await fetch_prices_for_symbol(async_session, symbol)
            if not df.empty:
                print(df.columns.tolist())
                daily_prices_df = transform_prices_to_daily(df)
                async with async_session() as session:
                    await session.bulk_insert_mappings(MultiplePricesTable, daily_prices_df.to_dict(orient="records"))
                    await session.commit()
    except Exception as e:
        logger.error(f"Error seeding daily adjusted prices table: {e}")
        raise

    logger.info(f"Seeding of daily adjusted prices table finished.")
