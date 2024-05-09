from abc import ABC, abstractmethod
from typing import Any


class FetchStatement(ABC):
	"""Abstract class for encapsulating data fetching parameters.
	This class must be extended with specific implementations that format or validate queries."""

	def __init__(self):
		self._query = str
		self._parameters = tuple

	@property
	def query(self) -> str:
		return self._query

	@property
	@abstractmethod
	def parameters(self) -> Any:
		"""Abstract property to ensure parameters are returned in an expected sequence type, specifically a tuple."""
		pass
