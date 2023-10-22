"""
bla bla
"""
import logging
from src.seed_raw_data.schemas.files_mapping import FileTableMapping

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RollConfigService:
    async def process_roll_config(self, map_item: FileTableMapping):
        """
        bla bla
        """
