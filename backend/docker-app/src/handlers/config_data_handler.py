import logging
from src.db.schemas.config_schemas.instrument_config_schema import InstrumentConfigSchema
from src.db.schemas.config_schemas.instrument_metadata_schema import InstrumentMetadataSchema
from src.db.schemas.config_schemas.roll_config_schema import RollConfigSchema
from src.db.schemas.config_schemas.spread_cost_schema import SpreadCostSchema

from src.db.seed.data_preprocessor import DataPreprocessor

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigDataHandler:

    def __init__(self, config_schemas=None):
        if config_schemas is None:
            # Default schemas if none provided
            self.config_schemas = [
                InstrumentConfigSchema(),
                InstrumentMetadataSchema(),
                RollConfigSchema(),
                SpreadCostSchema()
            ]
        else:
            self.config_schemas = config_schemas

    def handle_data_processing(self):       
        for schema in self.config_schemas:
            try:
                self._process_config_schema(schema)
                logger.info(f"Data processing completed for schema: {schema.__class__.__name__}")
            except Exception as e:
                logger.error(f"Error processing data for schema {schema.__class__.__name__}: {e}")
                # You can choose to raise the exception or continue with the next schema
                continue

    def _process_config_schema(self, schema):
        preprocessor = DataPreprocessor(schema)
        data = preprocessor.load_file()  # Assuming visibility of load_files is public
        preprocessor.process_data(data)