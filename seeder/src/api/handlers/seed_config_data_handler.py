"""
This module contains the SeeConfigDataHandler class, 
which is responsible for seeding the database from CSV files.
"""

from common.src.logging.logger import AppLogger
from seeder.src.csv_to_db_configs.config_files_config import (
    InstrumentConfigConfig,
    InstrumentMetadataConfig,
    RollConfigConfig,
    SpreadCostConfig,
)
from seeder.src.services.instrument_config_seed_service import (
    InstrumentConfigSeedService,
)
from seeder.src.utils.csv_loader import get_full_path, load_csv

# from data_management.src.services.raw_data.instrument_config_services import (
#     InstrumentConfigService,
# )
# from data_management.src.services.raw_data.instrument_metadata_service import (
#     InstrumentMetadataService,
# )
# from data_management.src.services.raw_data.roll_config_service import RollConfigService
# from data_management.src.services.raw_data.spread_costs_service import SpreadCostService


class SeedConfigDataHandler:
    """
    This class provides methods to seed the database
    asynchronously from CSV files according to given schemas.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_seed_service = InstrumentConfigSeedService(db_session)
        # self.instrument_metadata_service = InstrumentMetadataService(db_session)
        # self.roll_config_service = RollConfigService(db_session)
        # self.spread_costs_service = SpreadCostService(db_session)

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
        for config in configs:
            await self._process_data_and_insert_them_into_db(config)

    async def _process_data_and_insert_them_into_db(self, config):
        """
        Data processing for CSV files.
        """
        table_name = config.tablename
        full_path = get_full_path(config.directory, config.file_name)
        raw_data = load_csv(full_path)

        if table_name == "instrument_config":
            await self.instrument_config_seed_service.seed_instrument_config(raw_data)
        # elif table_name == "instrument_metadata":
        #     await self.instrument_metadata_service.insert_instruments_metadata_async(
        #         raw_data
        #     )
        # elif table_name == "roll_config":
        #     await self.roll_config_service.insert_roll_config_async(raw_data)
        # elif table_name == "spread_costs":
        #     await self.spread_costs_service.insert_spread_costs_async(raw_data)
        else:
            raise ValueError(f"Unrecognized table name: {table_name}")
