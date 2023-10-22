"""
bla
"""
import os
import logging
from src.seed_raw_data.errors.table_to_db_errors import InvalidFileNameError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FilesHelper:

    def get_full_path(self, directory: str, file_name:str)-> str:
        """
        bla
        """
        full_path = os.path.join(directory, file_name)
        if not os.path.exists(full_path):
            raise InvalidFileNameError(f"File path {full_path} does not exist.")
        return full_path