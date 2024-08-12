from common.src.database.base_statements.fetch_statement import FetchStatement


class GetDenomPriceQuery(FetchStatement):
	def __init__(self, symbol: str):
		self._query = """
        SELECT time, price
        FROM multiple_prices
        WHERE symbol = $1
        ORDER BY time
        """
		self._parameters = (symbol,)

	@property
	def parameters(self) -> tuple:
		return self._parameters
