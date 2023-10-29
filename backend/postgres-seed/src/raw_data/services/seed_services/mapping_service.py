"""A module for mapping directories to tables using a JSON configuration file."""
import json
import logging
from typing import List

from src.raw_data.schemas.files_mapping import FileTableMapping
from src.raw_data.errors.mapping_error import MappingNotFoundError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MappingService:
    """
    A service class for mapping directories to tables.
    """

    def __init__(self):
        self.json_file_path = "/home/app/mappings/files_to_tables_mapping.json"

    def load_mappings_from_json(self) -> List[FileTableMapping]:
        """
        Load directory-to-table mappings from a JSON file into a list of FileTableMapping objects.
        """
        try:
            with open(
                self.json_file_path, "r", encoding="utf-8"
            ) as file:  # Renamed 'f' to 'file'
                json_content = json.load(file)
            mappings = [FileTableMapping(**item) for item in json_content]
            logger.info("Successfully loaded mappings from JSON.")
            return mappings

        except FileNotFoundError:
            logger.error("File not found: %s", self.json_file_path)
            return []

        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from file: %s", self.json_file_path)
            return []

    def get_mapping_by_name(self, name: str) -> FileTableMapping:
        """
        Get the mapping by table name.
        """
        all_mappings = self.load_mappings_from_json()
        for mapping in all_mappings:
            if mapping.table == name:
                return mapping
        raise MappingNotFoundError(f"No mapping found for table name {name}")
