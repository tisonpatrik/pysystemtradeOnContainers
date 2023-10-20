"""
bla bla
"""
import logging

from src.csv_io.services.csv_files_service import CsvFilesService
from src.data_processor.services.data_processing_service import DataProcessingService

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TableToDBService:
    """
    bla bla
    """

    def __init__(self):
        self.csv_service = CsvFilesService()
        self.data_processing_service = DataProcessingService()

    async def insert_data_from_csv_to_table_async(self, map_item):
        """
        Asynchronously insert data from a CSV file to a database table.

        Args:
            directory (str): The directory where the CSV file is located.
            table (str): The name of the database table to insert data into.

        Returns:
            None
        """
        csv_files = await self.csv_service.load_csv_files_from_directory_async(map_item)

        # Step 3: Add data preprocessing using either an existing method or Pydantic
        processed_tables = await self.data_processing_service.process_csv_files_async(
            csv_files
        )
        # Step 4: Integrate the existing insert_dataframe_async method
        # TODO

        # Step 5: Implement error handling and logging
        # TODO

        pass
