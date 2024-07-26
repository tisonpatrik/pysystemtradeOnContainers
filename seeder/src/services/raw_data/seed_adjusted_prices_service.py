import pandas as pd
from pandera.errors import SchemaError
from pandera.typing import DataFrame

from common.src.database.base_statements.insert_statement import InsertManyStatement
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from seeder.src.db_models.db_models import AdjustedPricesModel
from seeder.src.schemas.raw_data_schemas import AdjustedPricesSchema


class SeedAdjustedPricesService:
    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def seed_adjusted_prices_async(self, raw_data: pd.DataFrame):
        try:
            date_time = AdjustedPricesSchema.date_time
            raw_data[date_time] = pd.to_datetime(raw_data[date_time])
            validated = DataFrame[AdjustedPricesSchema](raw_data)
            statement = InsertManyStatement(table_name=AdjustedPricesModel.__tablename__, data=validated)
            await self.repository.insert_dataframe_async(statement)
            self.logger.info(f"Successfully inserted {len(raw_data)} records into {AdjustedPricesModel.__name__}.")

        except SchemaError as schema_exc:
            self.logger.error(f"Schema validation error: {schema_exc.failure_cases}")
            raise
