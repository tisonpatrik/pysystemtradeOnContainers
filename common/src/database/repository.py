from typing import Any

from asyncpg.pool import Pool

from common.src.database.base_statements.fetch_statement import FetchStatement
from common.src.database.base_statements.insert_statement import (
    InsertManyStatement,
    InsertStatement,
)
from common.src.logging.logger import AppLogger


class Repository:
    def __init__(self, pool: Pool):
        self.pool = pool
        self.logger = AppLogger.get_instance().get_logger()

    async def fetch_item_async(self, statement: FetchStatement) -> Any | None:
        try:
            async with self.pool.acquire() as connection:
                prepared_stmt = await connection.prepare(statement.query)
                return await prepared_stmt.fetchrow(*statement.parameters)
        except Exception:
            self.logger.exception("Failed to fetch data with query %s", statement.query)
            raise

    async def fetch_many_async(self, statement: FetchStatement) -> list:
        try:
            async with self.pool.acquire() as connection:
                prepared_stmt = await connection.prepare(statement.query)
                return await prepared_stmt.fetch(*statement.parameters, timeout=60)
        except Exception:
            self.logger.exception("Failed to fetch data with query %s", statement.query)
            raise

    async def insert_dataframe_async(self, statement: InsertManyStatement) -> None:
        records = statement.get_records()
        columns = statement.get_columns()
        table_name = statement.get_table_name()
        batch_size: int = 1000000
        try:
            async with self.pool.acquire() as connection:
                for i in range(0, len(records), batch_size):
                    batch_records = records[i : i + batch_size]
                    async with connection.transaction():
                        await connection.copy_records_to_table(table_name=table_name, records=batch_records, columns=columns)
                    self.logger.info("Inserted batch %s with %u records into %v", i // batch_size + 1, len(batch_records), table_name)
        except Exception:
            self.logger.exception("Failed to insert data into the database")
            raise

    async def insert_item_async(self, statement: InsertStatement) -> None:
        query = statement.get_insert_query()
        values = statement.get_values()
        try:
            async with self.pool.acquire() as connection, connection.transaction():
                await connection.execute(query, *values)
        except Exception:
            self.logger.exception("Failed to insert data into the database")
            raise
