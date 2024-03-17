"""Module for calculating robust volatility for financial instruments."""

from typing import List

import pandas as pd
from pandera.errors import SchemaError
from pandera.typing import DataFrame

from common.src.database.entity_repository import EntityRepository
from common.src.database.records_repository import RecordsRepository
from common.src.db.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.converter import convert_frame_to_series, convert_series_to_frame
from common.src.utils.table_operations import (
    add_column_and_populate_it_by_value,
    rename_columns,
)
from raw_data.src.models.config_models import InstrumentConfig
from raw_data.src.models.raw_data_models import AdjustedPricesModel
from raw_data.src.schemas.raw_data_schemas import AdjustedPrices
from risk.src.estimators.daily_returns_volatility import DailyReturnsVolEstimator
from risk.src.models.risk_models import DailyReturnsVolatility
from risk.src.schemas.risk_schemas import DailyReturnsVolatilitySchema


class DailyReturnsVolSeedService:
    """Service for seeding daily returns volatility of financial instruments."""

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        # self.risk_repository = RecordsRepository(db_session, DailyReturnsVolatility)
        # self.instrument_repository = EntityRepository(db_session, InstrumentConfig)
        # self.prices_repository = RecordsRepository(db_session, AdjustedPricesModel)
        self.estimator = DailyReturnsVolEstimator()
        self.instrument_repository = Repository(db_session, InstrumentConfig)
        self.prices_repository = Repository(db_session, AdjustedPricesModel)

    async def seed_daily_returns_vol_async(self):
        """Seed daily returns volatility."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                DailyReturnsVolatility.__tablename__,
            )
            all_adjusted_prices = await self.prices_repository.fetch_data_to_df_async()
            instrument_configs = (
                await self.instrument_repository.fetch_data_to_df_async()
            )
            for config in instrument_configs.itertuples():
                symbol = str(config.symbol)

                # Filter for the current symbol
                adjusted_prices = all_adjusted_prices[
                    all_adjusted_prices[AdjustedPrices.symbol] == symbol
                ]

                prices = convert_frame_to_series(
                    adjusted_prices,
                    AdjustedPrices.date_time,
                    AdjustedPrices.price,
                )
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
            #     await self.repository.insert_many_async(
            #         validated, DailyReturnsVolatility.__tablename__
            #     )
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
