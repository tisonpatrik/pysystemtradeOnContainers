from typing import Union

import pandas as pd
from pydantic import BaseModel


class InsertManyStatement:
	"""Statement class for preparing data for insert operations. This class accepts either a pandas DataFrame or Series."""

	def __init__(self, table_name: str, data: Union[pd.DataFrame, pd.Series]):
		self._table_name = table_name
		self._data = data

	def get_records(self):
		"""Converts the data to a numpy array for insertion purposes."""
		return self._data.to_numpy()

	def get_columns(self) -> list[str]:
		"""Returns a list of column names from the data."""
		return self._data.columns.tolist()

	def get_table_name(self) -> str:
		"""Returns the table name."""
		return self._table_name


class InsertStatement:
	"""Statement class for preparing a single object for insert operations."""

	def __init__(self, table_name: str, data: BaseModel):
		self._table_name = table_name
		self._data = data

	def get_columns(self) -> list[str]:
		"""Returns a list of column names from the data."""
		return list(self._data.model_dump().keys())

	def get_values(self) -> list:
		"""Returns a list of values from the data."""
		return list(self._data.model_dump().values())

	def get_insert_query(self) -> str:
		"""Returns the SQL insert query string."""
		columns = ', '.join(self.get_columns())
		values_placeholders = ', '.join(f'${i+1}' for i in range(len(self.get_values())))
		query = f'INSERT INTO {self._table_name} ({columns}) VALUES ({values_placeholders})'
		return query
