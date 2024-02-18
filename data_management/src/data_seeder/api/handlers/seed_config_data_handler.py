"""
This module contains the SeeConfigDataHandler class, 
which is responsible for seeding the database from CSV files.
"""

from src.core.utils.logging import AppLogger
from src.data_seeder.csv_to_db_configs.config_files_config import (
    InstrumentConfigConfig,
    InstrumentMetadataConfig,
    RollConfigConfig,
    SpreadCostConfig,
)
from src.data_seeder.services.config_files_processing_service import (
    ConfigFilesSeedService,
)
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.raw_data.services.instrument_metadata_service import InstrumentMetadataService
from src.raw_data.services.roll_config_service import RollConfigService
from src.raw_data.services.spread_costs_service import SpreadCostService
from src.raw_data.services.tradable_instruments_service import (
    TradableInstrumentsService,
)


class SeeConfigDataHandler:
    """
    This class provides methods to seed the database
    asynchronously from CSV files according to given schemas.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.config_files_seed_service = ConfigFilesSeedService()
        self.tradable_instrument_service = TradableInstrumentsService(db_session)
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.instrument_metadata_service = InstrumentMetadataService(db_session)
        self.roll_config_service = RollConfigService(db_session)
        self.spread_costs_service = SpreadCostService(db_session)

    async def seed_data_from_csv_async(self):
        """
        Asynchronously seed the database from CSV files using predefined schemas.
        """
        self.logger.info("Data processing for csv files has started")
        configs = [
            InstrumentConfigConfig,
            InstrumentMetadataConfig,
            RollConfigConfig,
            SpreadCostConfig,
        ]
        list_of_instruments = (
            await self.tradable_instrument_service.get_tradable_instruments()
        )
        for config in configs:
            await self._process_data_and_insert_them_into_db(
                config, list_of_instruments
            )

    async def _process_data_and_insert_them_into_db(self, config, list_of_symbols):
        """
        Data processing for CSV files.
        """
        table_name = config.tablename
        if table_name == "instrument_config":
            column_names = self.instrument_config_service.get_names_of_columns()
            raw_data = self.config_files_seed_service.process_config_files(
                list_of_symbols, config, column_names
            )
            await self.instrument_config_service.insert_instruments_config_async(
                raw_data
            )
        elif table_name == "instrument_metadata":
            column_names = self.instrument_metadata_service.get_names_of_columns()
            raw_data = self.config_files_seed_service.process_config_files(
                list_of_symbols, config, column_names
            )
            await self.instrument_metadata_service.insert_instruments_metadata_async(
                raw_data
            )
        elif table_name == "roll_config":
            column_names = self.roll_config_service.get_names_of_columns()
            raw_data = self.config_files_seed_service.process_config_files(
                list_of_symbols, config, column_names
            )
            await self.roll_config_service.insert_roll_config_async(raw_data)
        elif table_name == "spread_cost":
            column_names = self.spread_costs_service.get_names_of_columns()
            raw_data = self.config_files_seed_service.process_config_files(
                list_of_symbols, config, column_names
            )
            await self.spread_costs_service.insert_spread_costs_async(raw_data)
        else:
            raise ValueError(f"Unrecognized table name: {table_name}")
