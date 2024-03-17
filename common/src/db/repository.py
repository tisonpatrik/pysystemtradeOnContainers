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
                df = pd.DataFrame([dict(record) for record in records])
                self.logger.info(
                    f"Fetched data from {self.entity_class.__tablename__} into DataFrame"
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

    async def new_fetch_data_to_df_async(self) -> pd.DataFrame:
        """
        Fetches all data from the entity's table asynchronously using a cursor
        and loads it into a pandas DataFrame for efficient memory usage.
        Utilizes connection pooling for improved performance and security.
        """
        async with self.conn.transaction():
            # Use a cursor for efficient row fetching
            cursor = await self.conn.cursor(
                f'SELECT * FROM "{self.entity_class.__tablename__}";'
            )
            records = []
            async for record in cursor:
                records.append(dict(record))

        if records:
            df = pd.DataFrame(records)
            self.logger.info(
                f"Fetched data from {self.entity_class.__tablename__} into DataFrame"
            )
        else:
            df = pd.DataFrame()
            self.logger.info(f"No data fetched from {self.entity_class.__tablename__}")

        return df
