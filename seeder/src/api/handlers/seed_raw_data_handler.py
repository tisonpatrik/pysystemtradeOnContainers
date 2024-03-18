"""
This module contains the SeedDBHandler class, 
which is responsible for seeding the database from CSV files.
"""

from src.csv_to_db_configs.raw_data_config import (AdjustedPricesConfig,
                                                   FxPricesSchemaConfig,
                                                   MultiplePricesConfig,
                                                   RollCalendarsConfig)
from src.services.raw_data.seed_adjusted_prices_service import \
    SeedAdjustedPricesService
from src.services.raw_data.seed_fx_prices_service import SeedFxPricesService
from src.services.raw_data.seed_multiple_prices_service import \
    SeedMultiplePricesService
from src.services.raw_data.seed_roll_calendars_service import \
    SeedRollCalendarsService
from src.utils.csv_loader import get_full_path, load_csv

from common.src.logging.logger import AppLogger


class SeedRawDataHandler:
    """
    This class provides methods to seed the database
    asynchronously from CSV files according to given schemas.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.adjusted_prices_service = SeedAdjustedPricesService(db_session)
        self.fx_prices_service = SeedFxPricesService(db_session)
        self.multiple_prices_service = SeedMultiplePricesService(db_session)
        self.roll_calendars_service = SeedRollCalendarsService(db_session)

    async def seed_data_from_csv_async(self):
        """
        Asynchronously seed the database from CSV files using predefined schemas.
        """
        self.logger.info("Data processing for csv files has started")
        configs = [
            AdjustedPricesConfig,
            # FxPricesSchemaConfig,
            # MultiplePricesConfig,
            # RollCalendarsConfig,
        ]

        for config in configs:
            await self._process_data_and_insert_them_into_db(config)

    async def _process_data_and_insert_them_into_db(self, config):
        """
        Data processing for CSV files.
        """
        table_name = config.tablename
        full_path = get_full_path(config.directory, config.file_name)
        raw_data = load_csv(full_path)
        if table_name == "adjusted_prices":
            await self.adjusted_prices_service.seed_adjusted_prices_async(raw_data)
        elif table_name == "fx_prices":
            await self.fx_prices_service.seed_fx_prices_async(raw_data)

        elif table_name == "roll_calendars":
            await self.roll_calendars_service.seed_roll_calendars_service_async(
                raw_data
            )
        elif table_name == "multiple_prices":
            await self.multiple_prices_service.seed_multiple_prices_service_async(
                raw_data
            )
        else:
            raise ValueError(f"Unrecognized table name: {table_name}")
