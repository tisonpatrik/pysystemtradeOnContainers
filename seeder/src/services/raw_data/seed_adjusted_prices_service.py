import pandas as pd
from pandera.errors import SchemaError
from pandera.typing import DataFrame
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.database.records_repository import RecordsRepository
from common.src.logging.logger import AppLogger
from raw_data.src.models.raw_data_models import AdjustedPrices
from raw_data.src.schemas.raw_data_schemas import AdjustedPricesSchema


class SeedAdjustedPricesService:

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = RecordsRepository(db_session, AdjustedPrices)

    async def seed_adjusted_prices_async(self, raw_data: pd.DataFrame):
        try:
            date_time = AdjustedPricesSchema.date_time
            raw_data[date_time] = pd.to_datetime(raw_data[date_time])
            validated = DataFrame[AdjustedPricesSchema](raw_data)
            await self.repository.async_insert_dataframe_to_table(validated)
            self.logger.info(
                f"Successfully inserted {len(raw_data)} records into {AdjustedPrices.__name__}."
            )

        except SchemaError as schema_exc:
            self.logger.error(f"Schema validation error: {schema_exc}")
        except Exception as exc:
            self.logger.error(
                f"Error inserting data for {AdjustedPrices.__name__}: {str(exc)}"
            )
