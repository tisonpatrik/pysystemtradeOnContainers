from asyncpg import Connection
from asyncpg.exceptions import PostgresError

from common.src.database.statement import Statement
from common.src.logging.logger import AppLogger


class StatementFactory:

    def __init__(self, conn: Connection):
        self.conn = conn
        self.logger = AppLogger.get_instance().get_logger()

    async def create_fetch_many_statement(self, query: str) -> Statement:
        try:
            prepared_statement = await self.conn.prepare(query)
            return Statement(prepared_statement)
        except PostgresError as e:
            self.logger.error(f"Failed to prepare statement: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise e
