from typing import Generic, Type, TypeVar

from asyncpg import Connection
from asyncpg.exceptions import PostgresError

from common.src.database.base_model import BaseModel
from common.src.database.statement import Statement
from common.src.logging.logger import AppLogger

T = TypeVar("T", bound=BaseModel)


class StatementFactory(Generic[T]):

    def __init__(self, conn: Connection, model: Type[T]):
        self.conn = conn
        self.logger = AppLogger.get_instance().get_logger()
        self.table_name = model.__tablename__

    async def create_fetch_all_statement(self, columns: list[str]) -> Statement:
        column_names = ", ".join(columns)
        query = f"SELECT {column_names} FROM {self.table_name}"
        try:
            prepared_statement = await self.conn.prepare(query)
            return Statement(prepared_statement)
        except PostgresError as e:
            self.logger.error(f"Failed to prepare statement: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise e

    async def create_fetch_statement_with_where(self, columns: list[str], where_clause: str) -> Statement:
        """
        Creates a prepared statement for fetching records with a WHERE clause.

        :param columns: List of column names to fetch.
        :param where_clause: The WHERE clause string, with placeholders for parameters.
        """
        column_names = ", ".join(columns)
        query = f"SELECT {column_names} FROM {self.table_name} WHERE {where_clause}"
        try:
            prepared_statement = await self.conn.prepare(query)
            return Statement(prepared_statement)
        except PostgresError as e:
            self.logger.error(f"Failed to prepare statement: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise e
