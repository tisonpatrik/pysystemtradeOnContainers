import pandas as pd
from pandera.errors import SchemaError
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.models.raw_data_models import FxPrices
from raw_data.src.schemas.raw_data_schemas import FxPricesSchema


class SeedFxPricesService:
    """
    Service for dealing with operations related to fx prices.
    """

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = Repository(db_session, FxPrices)

    async def seed_fx_prices_async(self, raw_data: pd.DataFrame):
        """
        Insert fx prices data into db.
        """
        try:
            date_time = inspect(FxPrices).c.date_time.key
            raw_data[date_time] = pd.to_datetime(raw_data[date_time])
            FxPricesSchema.validate(raw_data, lazy=True)
            data_models = [FxPrices(**row.to_dict()) for _, row in raw_data.iterrows()]
            await self.repository.insert_many_async(data_models)
            self.logger.info(
                f"Successfully inserted {len(data_models)} records into {FxPrices.__tablename__}."
            )

        except SchemaError as schema_exc:
            # Log schema validation errors specifically
            self.logger.error(f"Schema validation error: {schema_exc}")
        except Exception as exc:
            # Log unexpected errors
            self.logger.error(
                f"Error inserting data for {FxPrices.__tablename__}: {str(exc)}"
            )
