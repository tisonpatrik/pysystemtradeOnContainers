from common.src.queries.base_statements.fetch_statement import FetchStatement
from common.src.validation.point_size import PointSize


class GetPointSize(FetchStatement):
	def __init__(self, symbol: str):
		self._query = """
        SELECT pointsize 
        FROM instrument_config 
        WHERE symbol = $1
        """
		self._parameters = (symbol,)
		self._output_type = PointSize

	@property
	def parameters(self) -> tuple:
		"""Implement the abstract property to return parameters as a tuple."""
		return (self._parameters,)
