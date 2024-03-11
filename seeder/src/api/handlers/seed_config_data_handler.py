"""
This module contains the SeeConfigDataHandler class, 
which is responsible for seeding the database from CSV files.
"""

from src.csv_to_db_configs.config_files_config import (
    InstrumentConfigConfig,
    InstrumentMetadataConfig,
    RollConfigConfig,
    SpreadCostConfig,
)
from src.services.config.instrument_config_seed_service import (
    InstrumentConfigSeedService,
)
from src.services.config.instrument_metadata_seed_service import (
    InstrumentMetadataSeedService,
)
from src.services.config.roll_config_seed_service import RollConfigSeedService
from src.services.config.spread_cost_seed_service import SpreadCostSeedService
from src.utils.csv_loader import get_full_path, load_csv

from common.src.logging.logger import AppLogger


class SeedConfigDataHandler:
    """
    This class provides methods to seed the database
    asynchronously from CSV files according to given schemas.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_seed_service = InstrumentConfigSeedService(db_session)
        self.instrument_metadata_seed_service = InstrumentMetadataSeedService(
            db_session
        )
        self.roll_config_seed_service = RollConfigSeedService(db_session)
        self.spread_cost_seed_service = SpreadCostSeedService(db_session)

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
            await self.instrument_config_seed_service.seed_instrument_config_async(
                raw_data
            )
        elif table_name == "instrument_metadata":
            await self.instrument_metadata_seed_service.seed_instrument_metadata_async(
                raw_data
            )
        elif table_name == "roll_config":
            await self.roll_config_seed_service.seed_roll_config_async(raw_data)
        elif table_name == "spread_costs":
            await self.spread_cost_seed_service.seed_spread_costs_async(raw_data)
        else:
            raise ValueError(f"Unrecognized table name: {table_name}")
