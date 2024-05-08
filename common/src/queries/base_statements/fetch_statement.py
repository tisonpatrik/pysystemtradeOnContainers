from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel


class FetchStatement(ABC):
	"""Abstract class for encapsulating data fetching parameters.
	This class must be extended with specific implementations that format or validate queries."""

	def __init__(self):
		self._query = str
		self._parameters = tuple
		self._output_type = BaseModel

	@property
	@abstractmethod
	def query(self) -> str:
		"""Abstract property to return the SQL query string."""
		pass

	@property
	@abstractmethod
	def parameters(self) -> tuple:
		"""Abstract property to ensure parameters are returned in an expected sequence type, specifically a tuple."""
		pass

	@property
	def output_type(self) -> Type[BaseModel]:
		return self._output_type
