from typing import Any

from asyncpg.pool import Pool

from common.src.database.base_statements.delete_statement import (
    DeleteStatement,
)
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
                record = await prepared_stmt.fetchrow(*statement.parameters)
                return record
        except Exception as e:
            self.logger.error(f"Failed to fetch data with query '{statement.query}': {e}")
            raise

    async def fetch_many_async(self, statement: FetchStatement) -> list:
        try:
            async with self.pool.acquire() as connection:
                prepared_stmt = await connection.prepare(statement.query)
                records = await prepared_stmt.fetch(*statement.parameters)
                return records
        except Exception as e:
            self.logger.error(f"Failed to fetch data with query '{statement.query}': {e}")
            raise

    async def insert_dataframe_async(self, statement: InsertManyStatement) -> None:
        records = statement.get_records()
        columns = statement.get_columns()
        table_name = statement.get_table_name()
        batch_size: int = 1000000
        try:
            async with self.pool.acquire() as connection:
                for i in range(0, len(records), batch_size):
                    batch_records = records[i:i + batch_size]
                    async with connection.transaction():
                        await connection.copy_records_to_table(
                            table_name=table_name,
                            records=batch_records,
                            columns=columns
                        )
                    self.logger.info(f"Inserted batch {i//batch_size + 1} with {len(batch_records)} records into {table_name}")
        except Exception as e:
            self.logger.error(f"Failed to insert data into the database: {str(e)}")
            raise

    async def insert_item_async(self, statement: InsertStatement) -> None:
        query = statement.get_insert_query()
        values = statement.get_values()
        try:
            async with self.pool.acquire() as connection, connection.transaction():
                await connection.execute(query, *values)
        except Exception as e:
            self.logger.error(f"Failed to insert data into the database: {str(e)}")
            raise

    async def delete_item_async(self, statement: DeleteStatement) -> None:
        query = statement.get_delete_query()
        values = statement.get_values()
        try:
            async with self.pool.acquire() as connection, connection.transaction():
                await connection.execute(query, *values)
                self.logger.info(f"Successfully deleted record from {statement._table_name} with condition: {statement._condition.json()}")
        except Exception as e:
            self.logger.error(f"Failed to delete data from the database: {str(e)}")
            raise
