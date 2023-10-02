import logging
 
from src.db.schemas.risk_schemas.robust_volatility import RobustVolatility
from src.db.repositories.data_loader import DataLoader
from src.db.repositories.data_inserter import DataInserter
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
        symbols = await self.get_all_symbols()
        adjusted_prices = await self.fetch_datasets_for_symbols(symbols)
        
        for data in adjusted_prices.items():
            # Calculate robust volatility
            volatility = robust_vol_calc(data)
            # Insert the volatility into the database
            await data_inserter.insert_dataframe_async(volatility, risk_schema.table_name)
    
    async def get_all_symbols(self):
        data_loader = DataLoader(self.database_url)
        query = "SELECT symbol FROM instrument_config"
        symbols_df = await data_loader.fetch_data_as_dataframe_async(query)
        return symbols_df

    async def fetch_datasets_for_symbols(self, symbols):
        datasets = {}
        data_loader = DataLoader(self.database_url)
        for symbol in symbols.items():
            
            query = f"SELECT * FROM adjusted_prices WHERE symbol = '{symbol}'"
            logger.debug(f"Executing query: {query}")

            try:
                adjusted_prices_data = await data_loader.fetch_data_as_dataframe_async(query)
                
                if adjusted_prices_data.empty:
                    logger.info(f"No data found for symbol: {symbol}")
                else:
                    datasets[symbol] = adjusted_prices_data
                    
            except Exception as e:
                logger.error(f"Error fetching data for symbol {symbol}: {e}")

        return datasets

