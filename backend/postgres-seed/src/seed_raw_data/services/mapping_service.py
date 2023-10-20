"""A module for mapping directories to tables using a JSON configuration file."""
import logging
import json
from typing import List

from src.seed_raw_data.schemas.files_mapping import FileTableMapping

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MappingService:
    """
    A service class for mapping directories to tables.
    """

    def __init__(self):
        self.json_file_path = "backend/postgres-seed/files_to_tables_mapping.json"

    def load_mappings_from_json(self) -> List[FileTableMapping]:
        """
        Load directory-to-table mappings from a JSON file into a list of FileTableMapping objects.

        Returns:
            List[FileTableMapping]: List of directory-to-table mappings
        """
        try:
            with open(self.json_file_path, "r", encoding="utf-8") as f:
                json_content = json.load(f)
            mappings = [FileTableMapping(**item) for item in json_content]
            logger.info("Successfully loaded mappings from JSON.")
            return mappings

        except FileNotFoundError:
            logger.error("File not found: %s", self.json_file_path)
            return []

        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from file: %s", self.json_file_path)
            return []

        except Exception as e:  # pylint: disable=broad-except
            logger.exception("An unexpected error occurred: %s", e)
            return []
