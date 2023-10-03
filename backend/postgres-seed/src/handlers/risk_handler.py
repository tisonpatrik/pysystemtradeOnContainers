import logging
import asyncio

import pandas as pd
from src.db.schemas.risk_schemas.robust_volatility import RobustVolatility
from src.db.repositories.data_loader import DataLoader
from src.db.repositories.data_inserter import DataInserter
from src.data_processing.data_frame_helper import convert_datetime_to_unixtime, concat_dataframes, split_dataframe, convert_column_to_datetime
from shared.src.estimators.volatility import robust_vol_calc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskHandler:

    def __init__(self, database_url):
        self.database_url = database_url

    async def calculate_and_insert_risk_for_all_dataset_async(self):
        """
        Asynchronously seed the risk values for all dataset.
       """
        data_inserter = DataInserter(self.database_url)
        risk_schema = RobustVolatility()
        adjusted_prices = await self.get_adjusted_prices_async()
        prices_by_symbol = self.split_dataframe_by_column(adjusted_prices)
        tasks = []

        for instrument_name, price_series in prices_by_symbol.items():
            task = asyncio.create_task(self.calculate_volatility_for_instrument_async(instrument_name, price_series))
            tasks.append(task)

        list_of_dfs = await asyncio.gather(*tasks)

        volatilities = concat_dataframes(list_of_dfs)
        # Insert the volatility into the database  
        await data_inserter.insert_dataframe_async(volatilities, risk_schema.table_name)

    async def calculate_volatility_for_instrument_async(self, instrument_name, price_series):
        volatility = robust_vol_calc(price_series).dropna()
        vol_df = volatility.reset_index()
        vol_df.columns = ['date_time', 'volatility']
        vol_df['symbol'] = instrument_name
        vol_df = convert_datetime_to_unixtime(vol_df)
        return vol_df

    async def get_adjusted_prices_async(self) -> pd.DataFrame:
        """Fetches adjusted prices from the database."""
        logger.info("Method get_adjusted_prices called.")
        data_loader = DataLoader(self.database_url)
        query = "SELECT * FROM adjusted_prices"
        try:
            df = await data_loader.fetch_data_as_dataframe_async(query)
            df = convert_column_to_datetime(df, 'unix_date_time')
            logger.info("Method get_adjusted_prices finished successfully.")
            return df
        except Exception as e:
            logger.error(f"Method get_adjusted_prices encountered an error: {e}")
            raise

    def split_dataframe_by_column(self, df):
        # Set datetime as the index
        df.set_index('datetime', inplace=True)
        
        # Use helper function to perform the generic task
        series_dict = split_dataframe(df, 'symbol')
        
        return series_dict
