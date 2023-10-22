"""
Provides utilities for reading CSV files.
"""
import logging
import pandas as pd
from src.csv_io.errors.csv_read_errors import CsvFileNotFoundException, CsvEmptyDataError, CsvParserError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CsvFilesService:
    """
    A class to work with CSV files asynchronously.
    """
    def load_csv(self, full_path) -> pd.DataFrame:
        """
        Loads a CSV file and returns a dataframe object.

        Args:
            full_path (str): The full path to the CSV file to be loaded.

        Returns:
            Dataframe representing the loaded CSV file.
        """
        try:
            df = pd.read_csv(full_path)
            return df
        except FileNotFoundError:
            logger.error("File not found: %s", full_path)
            raise CsvFileNotFoundException(f"File not found: {full_path}")
        except pd.errors.EmptyDataError:
            logger.error("No data: %s", full_path)
            raise CsvEmptyDataError(f"No data in file: {full_path}")
        except pd.errors.ParserError:
            logger.error("Error parsing file: %s", full_path)
            raise CsvParserError(f"Error parsing file: {full_path}")
        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise Exception(f"Unexpected error occurred: {e}")