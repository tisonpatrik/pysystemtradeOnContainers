"""Module for calculating robust volatility for financial instruments."""

from pandera.errors import SchemaErrors

from common.src.database.entity_repository import EntityRepository
from common.src.database.records_repository import RecordsRepository
from common.src.logging.logger import AppLogger
from common.src.validations.prices_schemas import DailyPrices
from raw_data.src.models.config_models import InstrumentConfig
from raw_data.src.models.raw_data_models import AdjustedPrices
from risk.src.estimators.daily_returns_volatility import DailyReturnsVolEstimator
from risk.src.models.risk_models import DailyReturnsVolatility


class DailyReturnsVolSeedService:
    """Service for seeding daily returns volatility of financial instruments."""

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.risk_repository = RecordsRepository(db_session, DailyReturnsVolatility)
        self.instrument_repository = EntityRepository(db_session, InstrumentConfig)
        self.prices_repository = RecordsRepository(db_session, AdjustedPrices)
        self.estimator = DailyReturnsVolEstimator()

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
                # daily_returns_vols = self.estimator.process_daily_returns_vol(
                #     transformed_df
                # )
                # print(daily_returns_vols.head())

                # validated = AdjustedPricesSchema.validate(prices, lazy=True)
                # await self.risk_repository.async_insert_dataframe_to_table(validated)
        except SchemaErrors as err:
            error_message = f"An error occurred during the daily returns volatility seeding process: {err}"
            self.logger.error(error_message)
            raise ValueError(error_message)
