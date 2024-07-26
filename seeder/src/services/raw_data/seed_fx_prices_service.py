import pandas as pd
from pandera.errors import SchemaError
from pandera.typing import DataFrame

from common.src.database.base_statements.insert_statement import InsertManyStatement
from common.src.database.repository import Repository
from seeder.src.db_models.db_models import FxPricesModel
from common.src.logging.logger import AppLogger
from seeder.src.schemas.raw_data_schemas import FxPricesSchema


class SeedFxPricesService:
    def __init__(self, repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def seed_fx_prices_async(self, raw_data: pd.DataFrame):
        try:
            date_time = FxPricesSchema.date_time
            raw_data[date_time] = pd.to_datetime(raw_data[date_time])
            validated = DataFrame[FxPricesSchema](raw_data)
            statement = InsertManyStatement(table_name=FxPricesModel.__tablename__, data=validated)
            await self.repository.insert_dataframe_async(statement)
            self.logger.info(f"Successfully inserted {len(raw_data)} records into {FxPricesModel.__name__}.")

        except SchemaError as schema_exc:
            self.logger.error(f"Schema validation error: {schema_exc.failure_cases}")
            raise
