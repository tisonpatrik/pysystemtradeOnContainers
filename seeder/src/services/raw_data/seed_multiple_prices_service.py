import pandas as pd
from pandera.errors import SchemaError
from pandera.typing import DataFrame

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.models.raw_data_models import MultiplePricesModel
from raw_data.src.schemas.raw_data_schemas import MultiplePricesSchema


class SeedMultiplePricesService:

    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def seed_multiple_prices_service_async(self, raw_data: pd.DataFrame):
        try:
            date_time = MultiplePricesSchema.date_time
            raw_data[date_time] = pd.to_datetime(raw_data[date_time])
            validated = DataFrame[MultiplePricesSchema](raw_data)
            await self.repository.insert_dataframe_async(validated)
            self.logger.info(f"Successfully inserted {len(raw_data)} records into {MultiplePricesModel.__name__}.")

        except SchemaError as schema_exc:
            self.logger.error(f"Schema validation error: {schema_exc.failure_cases}")
            raise
