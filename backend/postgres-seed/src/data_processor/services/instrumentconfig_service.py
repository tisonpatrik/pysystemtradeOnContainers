"""
bla bla
"""
import logging
from src.seed_raw_data.schemas.files_mapping import FileTableMapping

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InstrumentConfigService:
    async def process_instrument_config(self, map_item: FileTableMapping):
        """
        bla bla
        """
