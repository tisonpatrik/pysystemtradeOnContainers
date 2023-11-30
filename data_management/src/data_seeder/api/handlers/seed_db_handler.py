"""
This module contains the SeedDBHandler class, 
which is responsible for seeding the database from CSV files.
"""

from src.core.utils.logging import AppLogger
from src.data_seeder.services.config_files_seed_service import ConfigFilesService
from src.data_seeder.services.csv_loader_service import CsvLoaderService
from src.data_seeder.services.prices_seed_service import PricesSeedService
from src.raw_data.schemas.config_schemas import (
    InstrumentConfigSchema,
    RollConfigSchema,
    SpreadCostSchema,
)
from src.raw_data.schemas.raw_data_schemas import (
    AdjustedPricesSchema,
    FxPricesSchema,
    MultiplePricesSchema,
    RollCalendarsSchema,
)


class SeedDBHandler:
    """
    This class provides methods to seed the database
    asynchronously from CSV files according to given schemas.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.config_files_seed_service = ConfigFilesService(db_session)
        self.prices_seed_service = PricesSeedService(db_session)
        self.csv_loader = CsvLoaderService()

    async def insert_data_from_csv_async(self):
        """
        Asynchronously seed the database from CSV files using predefined schemas.
        """
        self.logger.info("Data processing for csv files has started")
        models = [
            InstrumentConfigSchema,
            RollConfigSchema,
            SpreadCostSchema,
            AdjustedPricesSchema,
            FxPricesSchema,
            MultiplePricesSchema,
            RollCalendarsSchema,
        ]

        list_of_instruments = self.csv_loader.get_csv_file_names_for_directory(
            AdjustedPricesSchema.directory
        )

        for model in models:
            await self._process_data_and_insert_them_into_db(model, list_of_instruments)

    async def _process_data_and_insert_them_into_db(self, model, list_of_symbols):
        """
        Data processing for CSV files.
        """
        table_name = model.tablename

        if table_name in ["instrument_config", "roll_config", "spread_cost"]:
            await self.config_files_seed_service.seed_config_files(
                list_of_symbols, model
            )
        elif table_name in [
            "adjusted_prices",
            "fx_prices",
            "multiple_prices",
            "roll_calendars",
        ]:
            await self.prices_seed_service.process_prices_files(model, list_of_symbols)
        else:
            raise ValueError(f"Unrecognized table name: {table_name}")
