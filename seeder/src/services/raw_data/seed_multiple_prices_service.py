import pandas as pd
from pandera.errors import SchemaError
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.models.raw_data_models import MultiplePrices
from raw_data.src.schemas.raw_data_schemas import MultiplePricesSchema


class SeedMultiplePricesService:

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = Repository(db_session, MultiplePrices)

    async def seed_multiple_prices_service_async(self, raw_data: pd.DataFrame):
        try:
            date_time = inspect(MultiplePrices).c.date_time.key
            raw_data[date_time] = pd.to_datetime(raw_data[date_time])
            MultiplePricesSchema.validate(raw_data, lazy=True)
            data_models = [
                MultiplePrices(**row.to_dict()) for _, row in raw_data.iterrows()
            ]
            await self.repository.insert_many_async(data_models)
            self.logger.info(
                f"Successfully inserted {len(data_models)} records into {MultiplePrices.__tablename__}."
            )

        except SchemaError as schema_exc:
            self.logger.error(f"Schema validation error: {schema_exc}")
        except Exception as exc:
            self.logger.error(
                f"Error inserting data for {MultiplePrices.__tablename__}: {str(exc)}"
            )
