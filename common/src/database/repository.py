from typing import Any

from asyncpg import Pool
from pydantic import BaseModel

from common.src.database.to_pydantic import convert_to_pydantic
from common.src.logging.logger import AppLogger
from common.src.queries.base_statements.fetch_statement import FetchStatement
from common.src.queries.base_statements.insert_statement import InsertStatement


class Repository:
	def __init__(self, pool: Pool):
		self.pool = pool
		self.logger = AppLogger.get_instance().get_logger()

	async def fetch_many_async(self, statement: FetchStatement) -> list[dict[Any, Any]]:
		try:
			async with self.pool.acquire() as connection:
				prepared_stmt = await connection.prepare(statement.query)
				records = await prepared_stmt.fetch(*statement.parameters)
				return [dict(record) for record in records]
		except Exception as e:
			self.logger.error(f"Failed to fetch data with query '{statement.query}': {e}")
			raise

	async def fetch_item_async(self, statement: FetchStatement) -> BaseModel:
		try:
			async with self.pool.acquire() as connection:
				prepared_stmt = await connection.prepare(statement.query)
				record = await prepared_stmt.fetchrow(*statement.parameters)
				typed = convert_to_pydantic(record, statement.output_type)
				return typed
		except Exception as e:
			self.logger.error(f"Failed to fetch data with query '{statement.query}': {e}")
			raise

	async def insert_dataframe_async(self, statement: InsertStatement) -> None:
		records = statement.get_records()
		columns = statement.get_columns()
		table_name = statement.get_table_name()

		try:
			async with self.pool.acquire() as connection, connection.transaction():
				await connection.copy_records_to_table(table_name=table_name, records=records, columns=columns)
		except Exception as e:
			self.logger.error(f'Failed to insert data into the database: {str(e)}')
