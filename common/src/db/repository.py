from typing import Generic, Type, TypeVar, Union

import pandas as pd
from asyncpg import Connection

from common.src.database.base_model import BaseEntity, BaseRecord
from common.src.logging.logger import AppLogger

T = TypeVar("T", bound=Union[BaseEntity, BaseRecord])


class Repository(Generic[T]):
    def __init__(self, conn: Connection, schema: Type[T]):
        self.conn = conn
        self.entity_class = schema
        self.logger = AppLogger.get_instance().get_logger()

    async def fetch_data_to_df_async(self) -> pd.DataFrame:
        """
        Fetches all data from the entity's table asynchronously and loads it into a pandas DataFrame.
        """
        try:
            query = f'SELECT * FROM "{self.entity_class.__tablename__}";'
            records = await self.conn.fetch(query)
            if records:
                columns = [key for key in records[0].keys()]
                df = pd.DataFrame.from_records(data=records, columns=columns)
                self.logger.info(
                    f"Fetched data from {self.entity_class.__tablename__} into DataFrame, total records: {len(records)}"
                )
                return df
            else:
                self.logger.info(
                    f"No data fetched from {self.entity_class.__tablename__}"
                )
                return pd.DataFrame()
        except Exception as e:
            self.logger.error(
                f"Error fetching data from {self.entity_class.__tablename__}: {e}"
            )
            raise
