from asyncpg import Connection
from asyncpg.exceptions import PostgresError
from asyncpg.prepared_stmt import PreparedStatement

from common.src.logging.logger import AppLogger


class StatementFactory():

    def __init__(self, conn: Connection, table_name: str):
        self.conn = conn
        self.logger = AppLogger.get_instance().get_logger()
        self.table_name = table_name

    async def create_fetch_all_statement(self, columns: list[str]) -> PreparedStatement:
        column_names = ', '.join(columns)
        query = f"SELECT {column_names} FROM {self.table_name}"
        try:
            return await self.conn.prepare(query)
        except PostgresError as e:
            self.logger.error(f"Failed to prepare statement: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise e