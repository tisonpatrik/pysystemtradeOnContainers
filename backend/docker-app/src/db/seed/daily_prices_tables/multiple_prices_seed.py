from src.db.repositories.repository import PostgresRepository
import pandas as pd
from pandas import DataFrame
import logging
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_all_symbols(repository: PostgresRepository) -> pd.DataFrame:
    """Retrieve all symbols from the instrument_config table."""
    try:
        parameters = {'TABLE': "instrument_config"}
        sql_template = f"SELECT * FROM {parameters['TABLE']}"
        data = await repository.load_data_async(sql_template, parameters)
        return data
    except Exception as e:
        logger.error(f"Error fetching symbols: {e}")
        raise

async def fetch_prices_for_symbol(repository: PostgresRepository, table: str, symbol: str) -> pd.DataFrame:
    """Fetch all prices for a given symbol from the specified table."""
    try:
        parameters = {'SYMBOL': symbol, 'TABLE': table}
        sql_template = f"SELECT * FROM {parameters['TABLE']} WHERE {parameters['SYMBOL']}"
        data = await repository.load_data_async(sql_template, parameters)
        
        # Check if the resulting data is empty. If so, return None or handle as needed.
        if data.empty:
            logger.warning(f"No data found for instrument {symbol}")
            return None
        
        return data
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

async def seed_daily_multiple_prices_table() -> None:
    """Main function to seed the daily multiple prices table."""
    logger.info(f"Seeding of daily multiple prices table started.")
    repository = PostgresRepository()
    try:
        symbols = await get_all_symbols(repository)
        for symbol in symbols:
            logger.info(f"Processing instrument: {symbol} of multiple prices table")
            raw_multiple_prices = await fetch_prices_for_symbol(repository,"raw_multiple_prices",symbol)
            raw_adjusted_prices = await fetch_prices_for_symbol(repository,"raw_adjusted_prices",symbol)
            raw_adjusted_prices.rename(columns={'PRICE': 'ADJUSTED_PRICE'}, inplace=True)

            df = raw_multiple_prices.merge(raw_adjusted_prices[['DATETIME', 'ADJUSTED_PRICE']], 
                                            on='DATETIME',
                                            how='left')
            if not df.empty:
                daily_prices_df = transform_prices_to_daily(df)
                repository.insert_data_async(daily_prices_df)
    except Exception as e:
        logger.error(f"Error seeding daily adjusted prices table: {e}")
        raise

    logger.info(f"Seeding of daily adjusted prices table finished.")
