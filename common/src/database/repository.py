from typing import Any

from asyncpg.exceptions import PostgresError
from asyncpg.pool import Pool

from common.src.database.base_statements.fetch_statement import FetchStatement
from common.src.database.base_statements.insert_statement import (
    InsertManyStatement,
    InsertStatement,
)
from common.src.database.errors.repository_errors import FetchError, InsertError
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
        except PostgresError as pg_err:
            self.logger.exception("Postgres error while fetching data with query: %s", statement.query)
            raise FetchError(f"Failed to fetch data: {pg_err}") from pg_err
        except Exception as err:
            self.logger.exception("Unexpected error while fetching data with query: %s", statement.query)
            raise FetchError(f"Unexpected error: {err}") from err

    async def fetch_many_async(self, statement: FetchStatement) -> list[Any]:
        try:
            async with self.pool.acquire() as connection:
                prepared_stmt = await connection.prepare(statement.query)
                return await prepared_stmt.fetch(*statement.parameters, timeout=60)
        except PostgresError as pg_err:
            self.logger.exception("Postgres error while fetching multiple records with query: %s", statement.query)
            raise FetchError(f"Failed to fetch multiple records: {pg_err}") from pg_err
        except Exception as err:
            self.logger.exception("Unexpected error while fetching multiple records with query: %s", statement.query)
            raise FetchError(f"Unexpected error: {err}") from err

    async def insert_dataframe_async(self, statement: InsertManyStatement) -> None:
        records = statement.get_records()
        columns = statement.get_columns()
        table_name = statement.get_table_name()
        batch_size: int = 1_000_000  # Use underscores for readability

        try:
            async with self.pool.acquire() as connection:
                for i in range(0, len(records), batch_size):
                    batch_records = records[i : i + batch_size]
                    async with connection.transaction():
                        await connection.copy_records_to_table(table_name=table_name, records=batch_records, columns=columns)
                    self.logger.info("Inserted batch %s with %u records into %s", (i // batch_size) + 1, len(batch_records), table_name)
        except PostgresError as pg_err:
            self.logger.exception("Postgres error while inserting data into table: %s", table_name)
            raise InsertError(f"Failed to insert data into {table_name}: {pg_err}") from pg_err
        except Exception as err:
            self.logger.exception("Unexpected error while inserting data into table: %s", table_name)
            raise InsertError(f"Unexpected error: {err}") from err

    async def insert_item_async(self, statement: InsertStatement) -> None:
        query = statement.get_insert_query()
        values = statement.get_values()

        try:
            async with self.pool.acquire() as connection, connection.transaction():
                await connection.execute(query, *values)
        except PostgresError as pg_err:
            self.logger.exception("Postgres error while inserting data with query: %s", query)
            raise InsertError(f"Failed to insert data: {pg_err}") from pg_err
        except Exception as err:
            self.logger.exception("Unexpected error while inserting data with query: %s", query)
            raise InsertError(f"Unexpected error: {err}") from err
