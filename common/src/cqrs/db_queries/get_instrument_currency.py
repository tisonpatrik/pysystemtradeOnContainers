from common.src.queries.db_queries.base_statements.fetch_statement import FetchStatement


class GetInstrumentCurrency(FetchStatement):
	"""
	A class to fetch the currency configuration for a given instrument symbol.
	"""

	def __init__(self, symbol: str):
		"""
		Initializes the query and parameters for fetching the instrument currency.

		:param symbol: The trading symbol of the instrument.
		"""
		self._query = """
        SELECT currency 
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
