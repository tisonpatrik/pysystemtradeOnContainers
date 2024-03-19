from typing import Tuple

import pandas as pd
from asyncpg import Connection
from asyncpg.exceptions import PostgresError
from asyncpg.prepared_stmt import PreparedStatement

from common.src.logging.logger import AppLogger


class StatementFactory():

    def __init__(self, conn: Connection):
        self.conn = conn
        self.logger = AppLogger.get_instance().get_logger()


    def prepare_data(self, dataframe: pd.DataFrame) -> list[Tuple]:
        """Converts a DataFrame to a list of tuples for database insertion. Raises an error if the dataframe is empty."""
        if dataframe.empty:
            error_message = "Dataframe is empty and cannot be prepared for insertion."
            self.logger.error(error_message)
            raise ValueError(error_message)
        
        try:
            return list(dataframe.itertuples(index=False, name=None))
        except Exception as e:
            self.logger.error(f"Error preparing data for insertion: {e}")
            raise
    

    async def create_insert_statement_async(self, table: str, columns: list[str]) -> PreparedStatement:
        """Creates an asynchronous insert statement for the specified table and columns."""
        try:
            placeholders = ', '.join(f'${i + 1}' for i in range(len(columns)))
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
            return await self.conn.prepare(query)
        except PostgresError as e:
            self.logger.error(f"Failed to prepare insert statement for {table}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in creating insert statement for {table}: {e}")
            raise
    

    # async def create_fetch_statement(self, conn: Connection, table: str, columns: list[str]) -> PreparedStatement:
    #     placeholders = ', '.join(f'${i+1}' for i, _ in enumerate(columns))
    #     query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    #     return await conn.prepare(query)