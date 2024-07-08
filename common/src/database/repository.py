from typing import Any

from asyncpg import Pool

from common.src.commands.db_commands.base_statements.insert_statement import InsertManyStatement, InsertStatement
from common.src.logging.logger import AppLogger
from common.src.queries.db_queries.base_statements.fetch_statement import FetchStatement


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

	async def fetch_many_async(self, statement: FetchStatement) -> list[dict[Any, Any]]:
		try:
			async with self.pool.acquire() as connection:
				prepared_stmt = await connection.prepare(statement.query)
				records = await prepared_stmt.fetch(*statement.parameters)
				return [dict(record) for record in records]
		except Exception as e:
			self.logger.error(f"Failed to fetch data with query '{statement.query}': {e}")
			raise

	async def insert_dataframe_async(self, statement: InsertManyStatement) -> None:
		records = statement.get_records()
		columns = statement.get_columns()
		table_name = statement.get_table_name()

		try:
			async with self.pool.acquire() as connection, connection.transaction():
				await connection.copy_records_to_table(table_name=table_name, records=records, columns=columns)
		except Exception as e:
			self.logger.error(f'Failed to insert data into the database: {str(e)}')

	async def insert_object_async(self, statement: InsertStatement) -> None:
		query = statement.get_insert_query()
		values = statement.get_values()
		try:
			async with self.pool.acquire() as connection, connection.transaction():
				await connection.execute(query, *values)
		except Exception as e:
			self.logger.error(f'Failed to insert data into the database: {str(e)}')
			raise
