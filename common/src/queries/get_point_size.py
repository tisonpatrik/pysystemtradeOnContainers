from common.src.queries.base_statements.fetch_statement import FetchStatement


class GetPointSize(FetchStatement):
	def __init__(self, symbol: str):
		self._query = """
        SELECT pointsize 
        FROM instrument_config 
        WHERE symbol = $1
        """
		self._parameters = (symbol,)

	@property
	def parameters(self) -> tuple:
		"""
		Returns the parameters to be used in the SQL query.

		:return: A tuple containing the parameters.
		"""
		return self._parameters
