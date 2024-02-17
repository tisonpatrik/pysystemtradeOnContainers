from src.core.utils.logging import AppLogger
from src.data_seeder.csv_to_db_configs.config_files_config import TradableInstruments
from src.data_seeder.services.tradable_instrument_seed_service import (
    TradableInstrumentsSeedService,
)


class SeedTradableInstrumentsHandler:
    """
    This class provides methods to seed the database table asynchronously from CSV file.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.tradable_instruments_service = TradableInstrumentsSeedService(db_session)

    async def seed_data_async(self):
        """
        Asynchronously seed the database table from CSV file using predefined schemas.
        """
        try:
            self.logger.info(
                "Data processing for tradable instruments files has started"
            )
            await self.tradable_instruments_service.seed_tradable_instruments_files(
                TradableInstruments
            )
            self.logger.info("Data processing completed successfully")
        except Exception as exc:
            self.logger.error("An error occurred during data processing: %s", str(exc))
            raise
