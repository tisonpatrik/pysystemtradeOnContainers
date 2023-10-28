"""
This module contains the FilePathValidator class, which is responsible for
validating file paths.
"""

import os
import logging
from src.raw_data.errors.table_to_db_errors import InvalidFileNameError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FilePathValidator:
    """
    The FilePathValidator class provides functionality for validating file paths.

    Attributes:
        None

    Methods:
        get_full_path(directory: str, file_name: str) -> str: Validates and returns the full file path.

    """

    def get_full_path(self, directory: str, file_name: str) -> str:
        """
        Validates the full file path constructed from the provided directory and file_name.

        Args:
            directory (str): The directory where the file is expected to be located.
            file_name (str): The name of the file.

        Returns:
            str: The full, validated file path.

        Raises:
            InvalidFileNameError: If the constructed full path does not exist.
        """
        full_path = os.path.join(directory, file_name)
        if not os.path.exists(full_path):
            raise InvalidFileNameError(f"File path {full_path} does not exist.")
        return full_path
