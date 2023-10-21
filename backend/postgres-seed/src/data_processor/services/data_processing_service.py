"""
bla bla
"""
import logging
from typing import List
from src.csv_io.schemas.csv_output import CsvOutput
from src.data_processor.services.mapping_service import MappingService
from src.data_processor.data_processing import pandas_helper

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessingService:
    """
    bla bla
    """

    def __init__(self):
        """
        bla bla
        """
        self.mapping_service = MappingService()

    async def process_csv_files_async(self, csv_files: List[CsvOutput]):
        """
        bla bla
        """
        mapping = self.mapping_service.load_mappings_from_json()
        data_frame = pandas_helper.convert_to_dataframe(csv_files)
