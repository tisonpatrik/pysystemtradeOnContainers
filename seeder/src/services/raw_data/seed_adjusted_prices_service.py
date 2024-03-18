import pandas as pd
from pandera.errors import SchemaError
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.db.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.models.raw_data_models import AdjustedPricesModel
from raw_data.src.schemas.adjusted_prices_schemas import AdjustedPricesSchema


class SeedAdjustedPricesService:

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = Repository(db_session, AdjustedPricesModel)

    async def seed_adjusted_prices_async(self, raw_data: pd.DataFrame):
        try:
            date_time = AdjustedPricesSchema.date_time
            raw_data[date_time] = pd.to_datetime(raw_data[date_time])
            AdjustedPricesSchema.validate(raw_data)
            data = list(map(lambda row: AdjustedPricesModel(**row[1].to_dict()), raw_data.iterrows()))
            # await self.repository.insert_data_async(data)
            self.logger.info(
                f"Successfully inserted {len(raw_data)} records into {AdjustedPricesModel.__name__}."
            )

        except SchemaError as schema_exc:
            self.logger.error(f"Schema validation error: {schema_exc.failure_cases}")
            raise
