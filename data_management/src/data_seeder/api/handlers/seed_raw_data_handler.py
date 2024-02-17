"""
This module contains the SeedDBHandler class, 
which is responsible for seeding the database from CSV files.
"""

from src.core.utils.logging import AppLogger
from src.data_seeder.csv_to_db_configs.config_files_config import (
    InstrumentConfigConfig,
    InstrumentMetadataConfig,
    RollConfigConfig,
    SpreadCostConfig,
)
from src.data_seeder.csv_to_db_configs.raw_data_config import (
    AdjustedPricesConfig,
    FxPricesSchemaConfig,
    MultiplePricesConfig,
    RollCalendarsConfig,
)
from src.data_seeder.services.config_files_processing_service import (
    ConfigFilesSeedService,
)
from src.data_seeder.services.prices_seed_service import PricesSeedService
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.raw_data.services.instrument_metadata_service import InstrumentMetadataService
from src.raw_data.services.roll_config_service import RollConfigService
from src.raw_data.services.tradable_instruments_service import (
    TradableInstrumentsService,
)


class SeedRawDataHandler:
    """
    This class provides methods to seed the database
    asynchronously from CSV files according to given schemas.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.config_files_seed_service = ConfigFilesSeedService()
        self.prices_seed_service = PricesSeedService(db_session)
        self.tradable_instrument_service = TradableInstrumentsService(db_session)
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.instrument_metadata_service = InstrumentMetadataService(db_session)
        self.roll_config_service = RollConfigService(db_session)

    async def seed_data_from_csv_async(self):
        """
        Asynchronously seed the database from CSV files using predefined schemas.
        """
        self.logger.info("Data processing for csv files has started")
        models = [
            InstrumentConfigConfig,
            InstrumentMetadataConfig,
            RollConfigConfig,
            SpreadCostConfig,
            FxPricesSchemaConfig,
            AdjustedPricesConfig,
            MultiplePricesConfig,
            RollCalendarsConfig,
        ]
        list_of_instruments = (
            await self.tradable_instrument_service.get_tradable_instruments()
        )
        for model in models:
            await self._process_data_and_insert_them_into_db(model, list_of_instruments)

    async def _process_data_and_insert_them_into_db(self, model, list_of_symbols):
        """
        Data processing for CSV files.
        """
        table_name = model.tablename
        raw_data = self.config_files_seed_service.process_config_files(
            list_of_symbols, model
        )
        if table_name == "instrument_config":
            await self.instrument_config_service.insert_instruments_config_async(
                raw_data
            )
        elif table_name == "instrument_metadata":
            await self.instrument_metadata_service.insert_instruments_metadata_async(
                raw_data
            )
        elif table_name == "roll_config":
            await self.roll_config_service.insert_roll_config_async(raw_data)

        elif table_name in [
            "fx_prices",
            "adjusted_prices",
            "multiple_prices",
            "roll_calendars",
        ]:
            await self.prices_seed_service.process_prices_files(model, list_of_symbols)
        else:
            raise ValueError(f"Unrecognized table name: {table_name}")
