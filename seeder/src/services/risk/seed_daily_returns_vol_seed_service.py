"""Module for calculating robust volatility for financial instruments."""

# from src.services.raw_data.adjusted_prices_service import AdjustedPricesService
# from src.services.raw_data.instrument_config_services import InstrumentConfigService
# from src.services.risk.daily_returns_volatility_service import DailyReturnsVolService

import pandas as pd
from sqlalchemy import inspect

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.models.config_models import InstrumentConfig
from raw_data.src.models.raw_data_models import AdjustedPrices
from risk.src.models.risk_models import DailyReturnsVolatility


class DailyReturnsVolSeedService:
    """Service for seeding daily returns volatility of financial instruments."""

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.risk_repository = Repository(db_session, DailyReturnsVolatility)
        self.prices_repository = Repository(db_session, AdjustedPrices)
        self.instrument_repository = Repository(db_session, InstrumentConfig)

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
                symbol_column = inspect(InstrumentConfig).c.symbol.key
                prices = await self.prices_repository.get_related_data_async(
                    filters={symbol_column: symbol}
                )
                data_frame = pd.DataFrame(prices)
                print(data_frame.head())

                # await self.daily_returns_vol_service.insert_daily_returns_vol_for_prices_async(
                #     daily_prices, symbol
                # )
        except Exception as error:
            error_message = f"An error occurred during the daily returns volatility seeding process: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)
