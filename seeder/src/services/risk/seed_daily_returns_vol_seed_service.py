"""Module for calculating robust volatility for financial instruments."""

# from src.services.raw_data.adjusted_prices_service import AdjustedPricesService
# from src.services.raw_data.instrument_config_services import InstrumentConfigService
# from src.services.risk.daily_returns_volatility_service import DailyReturnsVolService

import pandas as pd
from pandera.errors import SchemaErrors
from sqlalchemy import inspect

from common.src.database.entity_repository import EntityRepository
from common.src.database.records_repository import RecordsRepository
from common.src.logging.logger import AppLogger
from raw_data.src.models.config_models import InstrumentConfig
from raw_data.src.models.raw_data_models import AdjustedPrices
from raw_data.src.schemas.raw_data_schemas import AdjustedPricesSchema
from risk.src.models.risk_models import DailyReturnsVolatility


class DailyReturnsVolSeedService:
    """Service for seeding daily returns volatility of financial instruments."""

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.risk_repository = RecordsRepository(db_session, DailyReturnsVolatility)
        self.instrument_repository = EntityRepository(db_session, InstrumentConfig)
        self.prices_repository = RecordsRepository(db_session, AdjustedPrices)

        # self.instrument_config_service = InstrumentConfigService(db_session)
        # self.adjusted_prices_service = AdjustedPricesService(db_session)
        # self.daily_returns_vol_service = DailyReturnsVolService(db_session)

    async def seed_daily_returns_vol_async(self):
        """Seed daily returns volatility."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                DailyReturnsVolatility.__tablename__,
            )
            instrument_configs = await self.instrument_repository.get_all_async()
            for config in instrument_configs:
                symbol = config.symbol
                prices = await self.prices_repository.fetch_raw_data_from_table_by_symbol_async(
                    symbol
                )

                if prices.empty:
                    self.logger.info(f"DataFrame for symbol {symbol} is empty.")
                    continue
                AdjustedPricesSchema.validate(prices, lazy=True)

            # print(prices.head())

            # await self.daily_returns_vol_service.insert_daily_returns_vol_for_prices_async(
            #     daily_prices, symbol
            # )
        except SchemaErrors as err:
            # Logování specifických vadných řádků
            for index, failure_case in err.failure_cases.iterrows():
                error_detail = (
                    f"Chyba ve sloupci '{failure_case['column']}', "
                    f"chybná hodnota: {failure_case['failure_case']}, "
                    f"na indexu: {failure_case['index']}"
                )
                self.logger.error(error_detail)

            # Raisování vyjímky s celkovým sumářem chyb
            error_message = f"An error occurred during the daily returns volatility seeding process: {err}"
            self.logger.error(error_message)
            raise ValueError(error_message)
