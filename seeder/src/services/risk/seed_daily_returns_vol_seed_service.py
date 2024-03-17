"""Module for calculating robust volatility for financial instruments."""

from pandera.errors import SchemaError
from pandera.typing import DataFrame

from common.src.db.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_series_to_frame
from common.src.utils.table_operations import (
    add_column_and_populate_it_by_value,
    rename_columns,
)
from raw_data.src.models.config_models import InstrumentConfig
from raw_data.src.models.raw_data_models import AdjustedPricesModel
from raw_data.src.services.adjusted_prices_service import AdjustedPricesService
from risk.src.estimators.daily_returns_volatility import DailyReturnsVolEstimator
from risk.src.models.risk_models import DailyReturnsVolatility
from risk.src.schemas.risk_schemas import DailyReturnsVolatilitySchema


class DailyReturnsVolSeedService:
    """Service for seeding daily returns volatility of financial instruments."""

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.estimator = DailyReturnsVolEstimator()
        self.instrument_repository = Repository(db_session, InstrumentConfig)
        self.prices_repository = Repository(db_session, AdjustedPricesModel)
        self.risk_repository = Repository(db_session, DailyReturnsVolatility)
        self.prices_service = AdjustedPricesService(db_session)

    async def seed_daily_returns_vol_async(self):
        """Seed daily returns volatility."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                DailyReturnsVolatility.__tablename__,
            )

            instrument_configs = (
                await self.instrument_repository.fetch_data_to_df_async()
            )
            for config in instrument_configs.itertuples():
                symbol = str(config.symbol)
                prices = await self.prices_service.get_daily_prices_async(symbol)

                daily_returns_vols = self.estimator.process_daily_returns_vol(prices)
                framed = convert_series_to_frame(daily_returns_vols)
                populated = add_column_and_populate_it_by_value(
                    framed, DailyReturnsVolatilitySchema.symbol, symbol
                )
                renamed = rename_columns(
                    populated,
                    [
                        DailyReturnsVolatilitySchema.date_time,
                        DailyReturnsVolatilitySchema.daily_returns_volatility,
                        DailyReturnsVolatilitySchema.symbol,
                    ],
                )
                validated = DataFrame[DailyReturnsVolatilitySchema](renamed)
                # await self.repository.insert_many_async(
                #     validated, DailyReturnsVolatility.__tablename__
                # )
            self.logger.info(
                f"Successfully inserted {DailyReturnsVolatility.__name__} calculations for {len(instrument_configs)} instruments."
            )

        except SchemaError as schema_exc:
            self.logger.error(f"Schema validation error: {schema_exc.failure_cases}")
            raise

        except Exception as e:
            self.logger.error(
                "An unexpected error occurred during the seeding process: %s", str(e)
            )
            raise
