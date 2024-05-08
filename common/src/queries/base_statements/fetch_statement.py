from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class FetchStatement(Generic[T]):
	"""Abstract class for encapsulating data fetching parameters.
	This class must be extended with specific implementations that format or validate queries."""

	def __init__(self):
		self._query = str
		self._parameters = tuple
		self._output_type: Type[T] = BaseModel

	@property
	def query(self) -> str:
		"""Abstract property to return the SQL query string."""
		return self._query

	@property
	@abstractmethod
	def parameters(self) -> tuple:
		"""Abstract property to ensure parameters are returned in an expected sequence type, specifically a tuple."""
		pass

	@property
	def output_type(self) -> Type[BaseModel]:
		return self._output_type
