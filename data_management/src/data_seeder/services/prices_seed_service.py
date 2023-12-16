"""
This module provides a service for processing CSV files and returning adjusted pricing data.
It utilizes various helper classes for tasks such as file validation, date-time conversion,
and table adjustments.
"""

from src.core.utils.logging import AppLogger
from src.data_seeder.data_processors.prices_files_processor import PricesFilesProcessor
from src.data_seeder.errors.prices_data_seed_error import PricesFilesProcessingError
from src.data_seeder.services.csv_loader_service import CsvLoaderService
from src.data_seeder.utils.data_aggregators import concatenate_data_frames
from src.db.services.data_insert_service import DataInsertService


class PricesSeedService:
    """
    Manages the processing and adjustment of pricing data from CSV files.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.csv_loader_service = CsvLoaderService()
        self.prices_files_processor = PricesFilesProcessor(db_session)
        self.data_insert_service = DataInsertService(db_session)

    async def process_prices_files(self, model, list_of_symbols):
        """
        Process and prices for a given table mapping.
        """
        try:
            self.logger.info("Starting the process for %s table.", model.tablename)
            dataframes = self.csv_loader_service.load_multiple_csv_files(
                model.directory, list_of_symbols, model.ignore_symbols
            )
            processed_data_frames = self.prices_files_processor.process_price_files(
                model=model, dataframes=dataframes
            )
            price_data_frames = concatenate_data_frames(processed_data_frames)
            await self.data_insert_service.async_insert_dataframe_to_table(
                price_data_frames, model.tablename
            )
        except PricesFilesProcessingError as error:
            self.logger.error("An error occurred during processing: %s", error)
            raise
