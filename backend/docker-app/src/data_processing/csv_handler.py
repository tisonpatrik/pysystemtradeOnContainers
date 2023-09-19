import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CSVHandler:
    def load_csv(self, path: str) -> pd.DataFrame:
        """Load CSV file from the given path.
        Args:
            path (str): Path to the CSV file.

        Returns:
            pd.DataFrame: Loaded dataframe.
        """
        try:
            full_path = self._get_full_path(path)
            self.logger.info(f"Loading CSV file from {full_path}")
            return pd.read_csv(full_path)
        except Exception as e:
            self.logger.error(f"Error loading CSV file from {full_path}: {e}")
            raise

    def save_to_csv(self, df: pd.DataFrame, path: str):
        """Save dataframe to the given CSV path.

        Args:
            df (pd.DataFrame): Dataframe to save.
            path (str): Path to save the CSV file to.
        """
        try:
            full_path = self._get_full_path(path)
            df.to_csv(full_path, index=False)
            self.logger.info(f"Data saved to {full_path}")
        except Exception as e:
            self.logger.error(f"Error saving data to {full_path}: {e}")
            raise

    def _get_full_path(self, path: str) -> str:
        """Get the full path to a file, combining base and provided path."""
        return self.base_path + "/" + path