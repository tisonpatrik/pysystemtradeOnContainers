"""
bla bla
"""
import os
import logging

from src.seed_raw_data.schemas.files_mapping import FileTableMapping
from src.csv_io.services.csv_files_service import CsvFilesService
from src.data_processor.data_processing.tables_helper import TablesHelper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InstrumentConfigService:

    def __init__(self):
        self.csv_files_service = CsvFilesService()
        self.tables_helper = TablesHelper()

    async def process_instrument_config(self, map_item: FileTableMapping):
        """
        bla bla
        """
        full_path = os.path.join(map_item.directory, map_item.file_name)
        raw_data = self.csv_files_service.load_csv(full_path)
        renamed = self.tables_helper.rename_columns(raw_data, map_item.columns_mapping)
        


