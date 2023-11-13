import logging
import pandas as pd
from src.db.services.data_insert_service import DataInsertService
from src.raw_data.services.instrument_config_series import InstrumentConfigService
from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.raw_data.services.multiple_prices_service import MultiplePricesService
from src.risk.services.instrument_volatility import InstrumentVolatilityService

from src.core.models.risk_schemas import InstrumentVolatility
from src.core.models.config_schemas import InstrumentConfig


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstrumentVolatilityHandler:
    def __init__(self, db_session):
        self.db_session = db_session
        self.instrument_volatility_service = InstrumentVolatilityService()
        self.files_configs_service = InstrumentConfigService(self.db_session)
        self.data_inserter = DataInsertService(self.db_session)
        self.adjusted_service = AdjustedPricesService(self.db_session)
        self.multiple_prices_service = MultiplePricesService(self.db_session)
        self.table_name = InstrumentVolatility.__tablename__

    async def insert_robust_volatility_async(self):
        """
        Asynchronously fetches data from the specified table,
        performs date-time conversion, and inserts robust volatility data.
        """
        try:
            # symbols = await self.files_configs_service.get_list_of_symbols_async()
            symbols = pd.DataFrame({"symbol": ["AEX"]})
            for symbol in symbols.itertuples(index=False):
                symbol = symbol.symbol

                adjusted_prices = await self.adjusted_service.get_daily_prices_async(
                    symbol
                )
                if adjusted_prices.empty:
                    continue

                denominator_prices = (
                    await self.multiple_prices_service.get_denominator_prices_async(
                        symbol
                    )
                )
                point_size = (
                    await self.files_configs_service.get_point_size_for_symbol_async(
                        symbol
                    )
                )
                instrument_volatility = self.instrument_volatility_service.calculate_instrument_volatility_for_instrument(
                    denominator_prices,
                    adjusted_prices,
                    point_size[InstrumentConfig.pointsize.key].iloc[0],
                    symbol,
                )
                # await self.data_inserter.async_insert_dataframe_to_table(
                #     instrument_volatility, self.table_name
                # )
        except Exception as error:
            logger.error("Failed to insert robust volatility data: %s", error)
            raise
