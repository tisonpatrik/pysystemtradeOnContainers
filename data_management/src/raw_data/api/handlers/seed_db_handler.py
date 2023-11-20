"""
This module contains the SeedDBHandler class, 
which is responsible for seeding the database from CSV files.
"""

from src.core.errors.seeder_error import DataInsertionError
from src.db.services.data_insert_service import DataInsertService
from src.raw_data.models.config_models import InstrumentConfig, RollConfig, SpreadCost
from src.raw_data.models.raw_data_models import (
    AdjustedPrices,
    FxPrices,
    MultiplePrices,
    RollCalendars,
)
from src.raw_data.services.config_files_service import ConfigFilesService
from src.raw_data.services.csv_loader_service import CsvLoaderService
from src.raw_data.services.prices_service import PricesService
from src.raw_data.services.rollcalendars_service import RollCalendarsService
from src.utils.logging import AppLogger


class SeedDBHandler:
    """
    This class provides methods to seed the database
    asynchronously from CSV files according to given schemas.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.data_insert_service = DataInsertService(db_session)
        self.config_files_service = ConfigFilesService()
        self.prices_service = PricesService()
        self.rollcalendars_service = RollCalendarsService()
        self.csv_loader = CsvLoaderService()

    async def insert_data_from_csv_async(self):
        """
        Asynchronously seed the database from CSV files using predefined schemas.
        """
        self.logger.info("Data processing for csv files has started")
        models = [
            RollConfig,
            SpreadCost,
            AdjustedPrices,
            FxPrices,
            MultiplePrices,
            RollCalendars,
        ]

        list_of_instruments = self.csv_loader.get_csv_file_names_for_directory(
            AdjustedPrices.directory
        )
        # Process InstrumentConfig first
        await self._process_data_and_insert_them_into_db(
            InstrumentConfig, list_of_instruments
        )
        for model in models:
            await self._process_data_and_insert_them_into_db(model, list_of_instruments)

    async def _process_data_and_insert_them_into_db(self, model, list_of_symbols):
        try:
            instrument_config_data = self._get_processed_data_from_raw_file(
                model, list_of_symbols
            )
            await self.data_insert_service.async_insert_dataframe_to_table(
                instrument_config_data, model.__tablename__
            )
        except DataInsertionError as error:
            self.logger.error(
                f"Data insertion failed for {model.__tablename__}: {error}"
            )
            raise error

    def _get_processed_data_from_raw_file(self, model, list_of_symbols):
        """
        Data processing for CSV files.
        """
        if model.__tablename__ in ["instrument_config", "roll_config", "spread_cost"]:
            return self.config_files_service.process_config_files(
                model, list_of_symbols
            )
        if model.__tablename__ in ["adjusted_prices", "fx_prices", "multiple_prices"]:
            return self.prices_service.process_prices_files(model, list_of_symbols)
        if model.__tablename__ == "roll_calendars":
            return self.rollcalendars_service.process_roll_calendars(
                model, list_of_symbols
            )
        raise ValueError(f"Unrecognized table name: {model.__tablename__}")
