import logging

import pandas as pd
from src.db.schemas.risk_schemas.robust_volatility import RobustVolatility
from src.db.repositories.data_loader import DataLoader
from src.db.repositories.data_inserter import DataInserter
from src.data_processing.data_frame_helper import convert_datetime_to_unixtime, concat_dataframes
from shared.src.estimators.volatility import robust_vol_calc
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskHandler:

    def __init__(self, database_url):
        self.database_url = database_url

    async def calculate_and_insert_risk_for_all_dataset(self):
        """
        Asynchronously seed the risk values for all dataset.
       """
        data_inserter = DataInserter(self.database_url)
        risk_schema = RobustVolatility()
        adjusted_prices = await self.get_adujsted_prices()
        prices_by_symbol = self.split_dataframe_by_column(adjusted_prices)
        list_of_dfs = []
        for instrument_name, price_series in prices_by_symbol.items():
            # Calculate robust volatility
            volatility = robust_vol_calc(price_series).dropna()
            vol_df = volatility.reset_index()
            vol_df.columns = ['date_time', 'volatility']
            vol_df['symbol'] = instrument_name
            vol_df = convert_datetime_to_unixtime(vol_df)
            list_of_dfs.append(vol_df)

        volatilities = concat_dataframes(list_of_dfs)
        # Insert the volatility into the database  
        await data_inserter.insert_dataframe_async(volatilities, risk_schema.table_name)
    async def get_adujsted_prices(self):
        logger.info("Method get_adujsted_prices called.")
        
        data_loader = DataLoader(self.database_url)
        query = "SELECT * FROM adjusted_prices"
        
        try:
            df = await data_loader.fetch_data_as_dataframe_async(query)
             # Convert unix_date_time to datetime format
            df['datetime'] = pd.to_datetime(df['unix_date_time'], unit='s')
            
            logger.info("Method get_adujsted_prices finished successfully.")
            return df

        except Exception as e:
            logger.error(f"Method get_adujsted_prices encountered an error: {e}")


    def split_dataframe_by_column(self, df):
        # Use groupby to create a grouped object
        grouped = df.groupby('symbol')
        
        # Create an empty dictionary to store the resulting Series
        series_dict = {}
        
        for name, group in grouped:
            # Convert unix_date_time to datetime format
            group['datetime'] = pd.to_datetime(group['unix_date_time'], unit='s')
            
            # Set datetime as the index
            group.set_index('datetime', inplace=True)
            
            # Convert the 'price' column to a Pandas Series with datetime index
            price_series = pd.Series(group['price'].values, index=group.index)
            # Store this Series in the dictionary with symbol name as the key
            series_dict[name] = price_series

        return series_dict
