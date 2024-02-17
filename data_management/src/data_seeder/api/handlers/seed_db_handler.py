"""
This module contains the SeedDBHandler class, 
which is responsible for seeding the database from CSV files.
"""

from src.core.utils.logging import AppLogger
from src.data_seeder.csv_to_db_configs.config_files_config import (
    InstrumentConfigSchema,
    InstrumentMetadataSchema,
    RollConfigSchema,
    SpreadCostSchema,
)
from src.data_seeder.csv_to_db_configs.raw_data_config import (
    AdjustedPricesSchema,
    FxPricesSchema,
    MultiplePricesSchema,
    RollCalendarsSchema,
)
from src.data_seeder.services.config_files_seed_service import ConfigFilesSeedService
from src.data_seeder.services.prices_seed_service import PricesSeedService
from src.raw_data.services.tradable_instruments_service import (
    TradableInstrumentsService,
)


class SeedDBHandler:
    """
    This class provides methods to seed the database
    asynchronously from CSV files according to given schemas.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.config_files_seed_service = ConfigFilesSeedService(db_session)
        self.prices_seed_service = PricesSeedService(db_session)
        self.tradable_instrument_service = TradableInstrumentsService(db_session)

    async def insert_data_from_csv_async(self):
        """
        Asynchronously seed the database from CSV files using predefined schemas.
        """
        self.logger.info("Data processing for csv files has started")
        models = [
            InstrumentConfigSchema,
            InstrumentMetadataSchema,
            RollConfigSchema,
            SpreadCostSchema,
            FxPricesSchema,
            AdjustedPricesSchema,
            MultiplePricesSchema,
            RollCalendarsSchema,
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

        if table_name in [
            "instrument_config",
            "instrument_metadata",
            "roll_config",
            "spread_cost",
        ]:
            await self.config_files_seed_service.seed_config_files(
                list_of_symbols, model
            )
        elif table_name in [
            "fx_prices",
            "adjusted_prices",
            "multiple_prices",
            "roll_calendars",
        ]:
            await self.prices_seed_service.process_prices_files(model, list_of_symbols)
        else:
            raise ValueError(f"Unrecognized table name: {table_name}")
