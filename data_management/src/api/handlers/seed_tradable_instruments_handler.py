from src.app.csv_to_db_configs.config_files_config import TradableInstrumentsConfig
from src.services.raw_data.tradable_instruments_service import (
    TradableInstrumentsService,
)
from src.utils.csv_loader import get_full_path, load_csv

from common.logging.logger import AppLogger


class SeedTradableInstrumentsHandler:
    """
    This class provides methods to seed the database table asynchronously from CSV file.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.tradable_instruments_service = TradableInstrumentsService(db_session)

    async def seed_tradable_instruments_async(self):
        """
        Asynchronously seed the database table from CSV file using predefined schemas.
        """
        try:
            self.logger.info(
                "Data processing for tradable instruments files has started"
            )
            full_path = get_full_path(
                TradableInstrumentsConfig.directory, TradableInstrumentsConfig.file_name
            )
            raw_data = load_csv(full_path)
            await self.tradable_instruments_service.insert_tradable_instruments_async(
                raw_data
            )
            self.logger.info("Data processing completed successfully")
        except Exception as exc:
            self.logger.error("An error occurred during data processing: %s", str(exc))
            raise
