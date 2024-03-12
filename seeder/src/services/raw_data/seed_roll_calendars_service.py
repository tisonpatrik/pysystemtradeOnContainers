import pandas as pd
from pandera.errors import SchemaError
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.models.raw_data_models import RollCalendars
from raw_data.src.schemas.raw_data_schemas import RollCalendarsSchema


class SeedRollCalendarsService:

    def __init__(self, db_session: AsyncSession):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = Repository(db_session, RollCalendars)

    async def seed_roll_calendars_service_async(self, raw_data: pd.DataFrame):

        try:
            date_time = inspect(RollCalendars).c.date_time.key
            raw_data[date_time] = pd.to_datetime(raw_data[date_time])
            RollCalendarsSchema.validate(raw_data, lazy=True)
            data_models = [
                RollCalendars(**row.to_dict()) for _, row in raw_data.iterrows()
            ]
            await self.repository.insert_many_async(data_models)
            self.logger.info(
                f"Successfully inserted {len(data_models)} records into {RollCalendars.__tablename__}."
            )

        except SchemaError as schema_exc:
            self.logger.error(f"Schema validation error: {schema_exc}")
        except Exception as exc:
            self.logger.error(
                f"Error inserting data for {RollCalendars.__tablename__}: {str(exc)}"
            )
